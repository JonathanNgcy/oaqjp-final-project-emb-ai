"""Task 3: Parse Watson response text and format all five emotion scores."""

import json

import requests


def emotion_detector(text_to_analyze):
    """Return Watson emotion scores and the emotion with the maximum score."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(
        url, headers=headers, json={"raw_document": {"text": text_to_analyze}}, timeout=30
    )
    response.raise_for_status()
    scores = json.loads(response.text)["emotionPredictions"][0]["emotion"]
    result = {name: scores[name] for name in ("anger", "disgust", "fear", "joy", "sadness")}
    result["dominant_emotion"] = max(result, key=result.get)
    return result
