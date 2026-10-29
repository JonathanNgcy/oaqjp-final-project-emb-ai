"""Serve the course emotion detection interface with Flask on port 5000."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import EmotionServiceError, emotion_detector

app = Flask(__name__)


@app.route("/")
def index():
    """Render the supplied course interface."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze textToAnalyze and return the course's display sentence."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except EmotionServiceError:
        app.logger.exception("Watson emotion detection failed")
        # The supplied JavaScript displays response text only for HTTP 200.
        return "Emotion detection service unavailable. Please try again later."

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is 'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
        f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
        f"The dominant emotion is <b>{result['dominant_emotion']}</b>."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
