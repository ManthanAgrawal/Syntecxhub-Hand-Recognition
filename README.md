# Syntecxhub Project 2 - Hand Gesture Recognition

Real-time hand gesture recognition for the Syntecxhub Artificial Intelligence internship task. The app detects hand landmarks from a webcam, classifies simple gestures, and maps them to demo actions like play/pause, mute, volume control, and screenshot.

## Features

- Real-time hand landmark detection with MediaPipe
- OpenCV webcam interface with clean gesture/action overlay
- Gesture recognition for open palm, fist, thumbs up, peace, and point
- Gesture-to-action controller with cooldown protection
- Dry-run mode for safe demo recording
- Unit-tested classifier logic separated from the camera code

## Gesture Actions

| Gesture | Demo Action |
| --- | --- |
| Open Palm | Play/Pause |
| Fist | Mute |
| Thumbs Up | Volume Up |
| Peace | Volume Down |
| Point | Screenshot |

## Project Structure

```text
gesture_control/
  actions.py       # Maps recognized gestures to actions
  camera_app.py    # Webcam, MediaPipe, OpenCV drawing, and app loop
  gestures.py      # Pure gesture classification logic
tests/
  test_gestures.py # Unit tests for gesture recognition
run_demo.py        # Webcam demo entry point
requirements.txt   # Python dependencies
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run

Start in dry-run mode. It shows the detected gesture and mapped action without controlling your computer:

```bash
python run_demo.py --dry-run
```

Run with real media/volume actions:

```bash
python run_demo.py
```

Press `Q` in the webcam window to quit.

On Windows, the MediaPipe model is cached in `C:\tmp\syntecxhub_hand_gesture` so the demo also works when the project folder contains non-English characters.

## Demo

The repository includes a short demo video:

[Watch the demo](assets/demo.mp4)

## Test

```bash
python -m unittest discover
```

## Internship Requirement Coverage

- Uses MediaPipe to detect hand landmarks in real time
- Classifies simple gestures such as thumbs up, fist, and open palm
- Maps gestures to actions as a working demo
- Provides a webcam demo script
- Includes clean source code and tests for GitHub submission
