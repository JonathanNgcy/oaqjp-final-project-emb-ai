"""Task 2: Return the embedded Watson Emotion Predict response text."""

import requests


def emotion_detector(text_to_analyze):
    """Send text to the course API and return its raw JSON response text."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(
        url, headers=headers, json={"raw_document": {"text": text_to_analyze}}, timeout=30
    )
    response.raise_for_status()
    return response.text
