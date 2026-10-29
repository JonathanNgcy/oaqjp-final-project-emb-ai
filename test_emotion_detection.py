"""Run the five required course tests against Watson inside Theia Lab."""

import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Check the actual model's dominant emotion for each course statement."""

    def test_joy(self):
        """Recognize the course's joyful statement."""
        self.assertEqual(emotion_detector("I am glad this happened")["dominant_emotion"], "joy")

    def test_anger(self):
        """Recognize the course's angry statement."""
        self.assertEqual(
            emotion_detector("I am really mad about this")["dominant_emotion"], "anger"
        )

    def test_disgust(self):
        """Recognize the course's disgusted statement."""
        self.assertEqual(
            emotion_detector("I feel disgusted just hearing about this")["dominant_emotion"],
            "disgust",
        )

    def test_sadness(self):
        """Recognize the course's sad statement."""
        self.assertEqual(emotion_detector("I am so sad about this")["dominant_emotion"], "sadness")

    def test_fear(self):
        """Recognize the course's fearful statement."""
        self.assertEqual(
            emotion_detector("I am really afraid that this will happen")["dominant_emotion"],
            "fear",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
