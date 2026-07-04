# Syntecxhub Project 2 - Hand Gesture Recognition

Real-time hand gesture recognition built for the Syntecxhub Artificial Intelligence internship task. The project uses MediaPipe hand landmarks, classifies simple gestures, and maps them to demo actions such as play/pause, mute, and volume control.

## Highlights

- Real-time webcam detection with MediaPipe Hands
- Gesture classifier for open palm, fist, thumbs up, peace, and point
- Action mapping demo with cooldown protection
- Dry-run mode for safe demos without sending keyboard shortcuts
- Testable gesture logic separated from camera and UI code
- Clean OpenCV overlay for a portfolio-friendly demo

## Gesture Actions

| Gesture | Meaning | Demo Action |
| --- | --- | --- |
| Open Palm | All fingers extended | Play/Pause |
| Fist | All fingers folded | Mute |
| Thumbs Up | Thumb raised, fingers folded | Volume Up |
| Peace | Index and middle fingers extended | Volume Down |
| Point | Index finger extended | Screenshot |

## Project Structure

```text
gesture_control/
  actions.py       # Gesture-to-action mapping
  camera_app.py    # Webcam, MediaPipe, and OpenCV UI
  gestures.py      # Landmark-based gesture classifier
tests/
  test_gestures.py # Unit tests for classifier logic
run_demo.py        # Entry point for the webcam demo
requirements.txt   # Runtime dependencies
```

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run The Demo

Use dry-run mode first. It recognizes gestures and shows the mapped action without controlling your system:

```bash
python run_demo.py --dry-run
```

To enable media/volume keyboard actions:

```bash
python run_demo.py
```

Press `Q` in the webcam window to exit.

On Windows, the MediaPipe model is cached in `C:\tmp\syntecxhub_hand_gesture` so the demo also works when the project folder contains non-English characters.

## Demo

The repository includes a short demo video:

[Watch the demo](assets/demo.mp4)

## Run Tests

```bash
python -m unittest discover
```

## Internship Requirement Coverage

- Detects hand landmarks in real time using MediaPipe
- Classifies simple gestures including thumbs up, fist, and open palm
- Maps gestures to actions as a demo
- Exports a webcam demo script
- Includes clean source structure and tests for GitHub submission
