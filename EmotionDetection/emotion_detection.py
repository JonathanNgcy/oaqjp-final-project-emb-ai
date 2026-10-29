"""Detect five emotions with the course's embedded Watson NLP service."""

import json
import math

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


class EmotionServiceError(RuntimeError):
    """Indicate an unavailable service or an invalid Watson response."""


def emotion_detector(text_to_analyze):
    """Return emotion scores and their maximum, or all None for invalid text.

    HTTP 400 is the course API's invalid-input response. Network errors,
    other HTTP failures, and malformed predictions raise EmotionServiceError.
    Equal maximum scores use the order in EMOTIONS to break ties.
    """
    empty_result = dict.fromkeys((*EMOTIONS, "dominant_emotion"))
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result

    try:
        response = requests.post(
            URL,
            headers=HEADERS,
            json={"raw_document": {"text": text_to_analyze}},
            timeout=30,
        )
        if response.status_code == 400:
            return empty_result
        response.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise EmotionServiceError("Watson emotion service is unavailable.") from error

    try:
        predictions = json.loads(response.text)["emotionPredictions"]
        scores = predictions[0]["emotion"]
        result = {emotion: scores[emotion] for emotion in EMOTIONS}
        if any(
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not math.isfinite(score)
            or not 0 <= score <= 1
            for score in result.values()
        ):
            raise ValueError("Emotion scores must be finite numbers between 0 and 1.")
    except (ValueError, KeyError, IndexError, TypeError) as error:
        raise EmotionServiceError("Watson returned an invalid prediction.") from error

    result["dominant_emotion"] = max(result, key=result.get)
    return result
