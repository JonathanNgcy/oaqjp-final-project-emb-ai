"""Test request formatting, error handling, and Flask without a live API."""

import json
import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import (
    EMOTIONS,
    HEADERS,
    URL,
    EmotionServiceError,
    emotion_detector,
)
from server import app

SCORES = dict(zip(EMOTIONS, (0.01, 0.02, 0.03, 0.90, 0.04)))
EMPTY = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
POST = "EmotionDetection.emotion_detection.requests.post"


def watson_response(scores=None):
    """Build an HTTP response with the actual Watson response structure."""
    response = Mock(status_code=200)
    response.text = json.dumps({"emotionPredictions": [{"emotion": scores or SCORES}]})
    return response


class TestOfflineDetector(unittest.TestCase):
    """Verify the API contract separately from the real model's predictions."""

    @patch(POST)
    def test_request_and_output(self, post):
        """Send the exact course URL, model header, and JSON envelope."""
        post.return_value = watson_response()
        self.assertEqual(emotion_detector("I love my life"), {**SCORES, "dominant_emotion": "joy"})
        post.assert_called_once_with(
            URL, headers=HEADERS, json={"raw_document": {"text": "I love my life"}}, timeout=30
        )

    @patch(POST)
    def test_empty_and_invalid_inputs(self, post):
        """Reject missing, whitespace-only, and non-string input locally."""
        for value in ("", " \n\t", None, 42, [], {}):
            with self.subTest(value=value):
                self.assertEqual(emotion_detector(value), EMPTY)
        post.assert_not_called()

    @patch(POST)
    def test_http_400(self, post):
        """Return all six None values for Watson's bad-request response."""
        post.return_value = Mock(status_code=400, text="Bad Request")
        self.assertEqual(emotion_detector("unusable input"), EMPTY)
        post.return_value.raise_for_status.assert_not_called()

    @patch(POST)
    def test_network_failures(self, post):
        """Distinguish service failures from invalid user input."""
        for error in (requests.Timeout(), requests.ConnectionError()):
            with self.subTest(error=type(error).__name__):
                post.side_effect = error
                with self.assertRaises(EmotionServiceError):
                    emotion_detector("hello")

    @patch(POST)
    def test_http_failure(self, post):
        """Surface server errors as service failures."""
        post.return_value = Mock(status_code=503)
        post.return_value.raise_for_status.side_effect = requests.HTTPError()
        with self.assertRaises(EmotionServiceError):
            emotion_detector("hello")

    @patch(POST)
    def test_malformed_payloads(self, post):
        """Reject invalid JSON, missing predictions, and invalid score values."""
        payloads = ["not json", "null", "{}", '{"emotionPredictions": []}']
        for bad_score in (None, "0.9", True, -1, 2, float("nan"), float("inf")):
            payloads.append(watson_response({**SCORES, "joy": bad_score}).text)
        payloads.append(watson_response({"joy": 1}).text)
        for payload in payloads:
            with self.subTest(payload=payload):
                post.return_value = Mock(status_code=200, text=payload)
                with self.assertRaises(EmotionServiceError):
                    emotion_detector("hello")

    @patch(POST)
    def test_each_dominant_emotion(self, post):
        """Choose the maximum score across each of the five emotion keys."""
        for emotion in EMOTIONS:
            with self.subTest(emotion=emotion):
                scores = dict.fromkeys(EMOTIONS, 0.01)
                scores[emotion] = 0.9
                post.return_value = watson_response(scores)
                self.assertEqual(emotion_detector("example")["dominant_emotion"], emotion)

    @patch(POST)
    def test_zero_and_tied_scores(self, post):
        """Return a deterministic emotion even when all scores are zero."""
        post.return_value = watson_response(dict.fromkeys(EMOTIONS, 0.0))
        self.assertEqual(emotion_detector("example")["dominant_emotion"], "anger")


class TestFlaskRoutes(unittest.TestCase):
    """Exercise the supplied interface and course route contract."""

    def setUp(self):
        """Create a test client without opening a network port."""
        self.client = app.test_client()

    def test_home_and_static_script(self):
        """Serve the unchanged starter page and JavaScript."""
        self.assertIn(b'id="textToAnalyze"', self.client.get("/").data)
        with self.client.get("/static/mywebscript.js") as response:
            self.assertIn(b"emotionDetector?textToAnalyze", response.data)

    @patch("server.emotion_detector")
    def test_formatted_output(self, detector):
        """Display all scores and the bold dominant emotion in a sentence."""
        detector.return_value = {**SCORES, "dominant_emotion": "joy"}
        response = self.client.get("/emotionDetector", query_string={"textToAnalyze": "a & b?"})
        detector.assert_called_once_with("a & b?")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "For the given statement, the system response is 'anger': 0.01, "
            "'disgust': 0.02, 'fear': 0.03, 'joy': 0.9 and 'sadness': 0.04. "
            "The dominant emotion is <b>joy</b>.",
        )

    def test_blank_and_missing_text(self):
        """Show the exact required invalid-input message."""
        for query in ({}, {"textToAnalyze": ""}, {"textToAnalyze": "   "}):
            with self.subTest(query=query):
                response = self.client.get("/emotionDetector", query_string=query)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")

    @patch("server.emotion_detector", return_value=EMPTY)
    def test_api_rejected_text(self, _detector):
        """Map Watson's HTTP 400 result to the required interface message."""
        response = self.client.get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.get_data(as_text=True), "Invalid text! Please try again!")

    @patch("server.app.logger.exception")
    @patch("server.emotion_detector", side_effect=EmotionServiceError("internal details"))
    def test_service_error_display(self, _detector, log_error):
        """Show a service message that the provided JavaScript can display."""
        response = self.client.get("/emotionDetector?textToAnalyze=hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "Emotion detection service unavailable. Please try again later.",
        )
        log_error.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
