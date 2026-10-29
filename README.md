# Final project

Watson NLP Emotion Detection final project for IBM's Python and Flask course.
Returns anger, disgust, fear, joy, sadness, and the dominant emotion.

The [actual course instructions](https://cf-courses-data.static.labs.skills.network/Ikq0b5aphFY8ilBIqdwA5A/Final-project-emb-ai-Mark-v1.md)
require live requests **inside Skills Network Theia Lab**. The Watson API is
restricted to that environment. No API key or separate Watson SDK is needed.

## Set up in the course lab

```bash
cd /home/project
git clone https://github.com/JonathanNgcy/oaqjp-final-project-emb-ai.git final_project
cd final_project
python3 -m pip install -r requirements-dev.txt
python3 run_course_checks.py
python3 server.py
```

Use Skills Network **Launch Application** with port **5000**. Try
`I think I am having fun`, then a blank entry. The first should show joy;
the second must show `Invalid text! Please try again!`.

The route is `GET /emotionDetector?textToAnalyze=...`. The supplied
`templates/index.html` and `static/mywebscript.js` are unchanged.

## Package and tests

```python
from EmotionDetection.emotion_detection import emotion_detector
print(emotion_detector("I hate working long hours"))
```

The package initializer imports the module and exports the function.
The course names the function **emotion_detector**, not emotion_detection.

```bash
# Five required tests against the real Watson model; run inside Theia.
python3 test_emotion_detection.py

# Thirteen isolated tests for request formatting, errors, and Flask.
python3 -m unittest -v test_offline

# Required static analysis; no lint rules are disabled.
python3 -m pylint server.py
```

Offline tests use mocked responses and do not prove model predictions.
`run_course_checks.py` saves actual live-check output in `submission/` and
stops on any failure.

Blank/missing text and Watson HTTP 400 return six `None` values. Other HTTP
errors, timeouts, and malformed responses raise `EmotionServiceError`.
Flask displays a separate service error message. Interface messages use HTTP
200 because the supplied JavaScript only displays successful responses.
Scores are validated and emotion names come from fixed keys.

## Submission files

`checkpoints/task2/emotion_detection.py` preserves the initial raw-response
version. `checkpoints/task3/emotion_detection.py` preserves the formatted
version. The final application lives in `EmotionDetection/`.

`run_course_checks.py` prepares code snippets and authentic terminal logs
with the lab's required base names. For the AI-graded path, use:

- [Task 1 README](https://github.com/JonathanNgcy/oaqjp-final-project-emb-ai/blob/main/README.md)
- [Task 4 initializer](https://github.com/JonathanNgcy/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py)

Capture the actual deployed interface as `6b_deployment_test.png` and
`7c_error_handling_interface.png`. The peer-graded path also needs screenshots
of the folder, source files, and terminal outputs listed in the lab. Text logs
do not replace required screenshots. Mocked output is not live Watson evidence.

The lab filesystem is temporary. This GitHub repository and the local backup
preserve the code; download new screenshots and logs before leaving the lab.

Starter: [IBM repository](https://github.com/ibm-developer-skills-network/oaqjp-final-project-emb-ai),
commit `3e04588b7b73640f1afb806d3e6bf3e2a41e8fd2`. Original Apache license retained.
