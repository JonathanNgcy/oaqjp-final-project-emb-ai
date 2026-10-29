# Final project — submission guide

All live results here were produced in Skills Network Theia Lab on
October 29, 2026, at about 2:36 p.m. America/Toronto. No live result was mocked.
The project follows the lab's **Option 1: AI-Graded Submission and Evaluation**.

| Task | Submit |
| --- | --- |
| 1 | [Public README URL](https://github.com/JonathanNgcy/oaqjp-final-project-emb-ai/blob/main/README.md) |
| 2, Activity 1 | `2a_emotion_detection.txt` — initial function returning response.text |
| 2, Activity 2 | `2b_application_creation.txt` — actual raw Watson output |
| 3, Activity 1 | `3a_output_formatting.txt` — formatted function |
| 3, Activity 2 | `3b_formatted_output_test.txt` — joy verified |
| 4, Activity 1 | [Public initializer URL](https://github.com/JonathanNgcy/oaqjp-final-project-emb-ai/blob/main/EmotionDetection/__init__.py) |
| 4, Activity 2 | `4b_packaging_test.txt` — packaged import and anger verified |
| 5, Activity 1 | `5a_unit_testing.txt` — five required live tests |
| 5, Activity 2 | `5b_unit_testing_result.txt` — all five pass |
| 6, Activity 1 | `6a_server.txt` — Flask routes and output sentence |
| 6, Activity 2 | `6b_deployment_test.png` — actual deployed interface showing joy |
| 7, Activity 1 | `7a_error_handling_function.txt` — HTTP 400 returns all None |
| 7, Activity 2 | `7b_error_handling_server.txt` — exact invalid-text message |
| 7, Activity 3 | `7c_error_handling_interface.png` — actual blank-input interface |
| 8, Activity 1 | `8a_server_modified.txt` — documented Flask source |
| 8, Activity 2 | `8b_static_code_analysis.txt` — server.py scores 10.00/10 |

The .txt files contain the snippets or actual terminal output to copy into
the assignment, rather than screenshots of text. The two .png files are real
browser captures, saved in the required PNG format without changing their content.
The separate peer-graded path requires additional screenshots; these text files
are prepared for the AI-graded path.

Additional verification: `offline_tests.txt` contains 13 passing isolated tests;
`7_http_400_check.txt` confirms the real Watson service returns HTTP 400 for
blank input. Offline tests are clearly separate from the five live model tests.

The app remains available through the lab's port 5000 launcher while the lab
and server are running. Restart with `python3 server.py` in `/home/project/final_project`.

No assignment has been submitted on your behalf.
