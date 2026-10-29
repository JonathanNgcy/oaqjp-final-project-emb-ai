"""Expose the Watson emotion detection module and function."""

from . import emotion_detection
from .emotion_detection import EmotionServiceError, emotion_detector

__all__ = ["emotion_detection", "emotion_detector", "EmotionServiceError"]
