import argparse
import os
import tempfile
from time import monotonic
from pathlib import Path
from typing import Iterable, Tuple
from urllib.request import urlretrieve

import cv2

from .actions import ActionController, ActionEvent
from .gestures import Landmark, gesture_label, recognize_gesture


MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)


def _runtime_dir() -> Path:
    if os.name == "nt":
        return Path("C:/tmp/syntecxhub_hand_gesture")
    return Path(tempfile.gettempdir()) / "syntecxhub_hand_gesture"


DEFAULT_MODEL_PATH = _runtime_dir() / "hand_landmarker.task"
HAND_CONNECTIONS = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (0, 17),
)

GESTURE_COLORS = {
    "open_palm": (62, 191, 121),
    "fist": (72, 118, 255),
    "thumbs_up": (0, 176, 240),
    "peace": (186, 104, 200),
    "point": (255, 183, 77),
    "unknown": (120, 120, 120),
}


def _prepare_runtime(model_path: Path) -> Path:
    runtime_dir = _runtime_dir()
    runtime_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(runtime_dir)

    if not model_path.is_absolute():
        model_path = runtime_dir / model_path
    return _ensure_model(model_path)


def _ensure_model(model_path: Path) -> Path:
    if model_path.exists():
        return model_path

    model_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading MediaPipe hand model to {model_path}...")
    urlretrieve(MODEL_URL, model_path)
    return model_path


def _to_landmarks(hand_landmarks) -> Iterable[Landmark]:
    for point in hand_landmarks:
        yield Landmark(point.x, point.y, point.z)


def _draw_landmarks(frame, hand_landmarks) -> None:
    height, width = frame.shape[:2]
    points = [(int(point.x * width), int(point.y * height)) for point in hand_landmarks]

    for start, end in HAND_CONNECTIONS:
        cv2.line(frame, points[start], points[end], (64, 214, 255), 2)

    for point in points:
        cv2.circle(frame, point, 4, (255, 255, 255), -1)
        cv2.circle(frame, point, 6, (30, 144, 255), 1)


def _draw_status(
    frame,
    gesture_name: str,
    confidence: float,
    action_event: ActionEvent | None,
) -> None:
    color = GESTURE_COLORS.get(gesture_name, GESTURE_COLORS["unknown"])
    label = f"{gesture_label(gesture_name)}  {confidence:.0%}"
    cv2.rectangle(frame, (18, 18), (430, 118), (20, 24, 32), -1)
    cv2.rectangle(frame, (18, 18), (430, 118), color, 2)
    cv2.putText(
        frame,
        label,
        (36, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2,
        cv2.LINE_AA,
    )

    action_text = "Action: waiting"
    if action_event:
        action_text = f"Action: {action_event.action} ({action_event.status})"
    cv2.putText(
        frame,
        action_text,
        (36, 94),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (230, 230, 230),
        1,
        cv2.LINE_AA,
    )


def run_webcam_demo(
    camera_index: int = 0,
    dry_run: bool = False,
    max_num_hands: int = 1,
    model_path: Path = DEFAULT_MODEL_PATH,
) -> None:
    model_path = _prepare_runtime(model_path)
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions

    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_path)),
        running_mode=vision.RunningMode.VIDEO,
        num_hands=max_num_hands,
        min_hand_detection_confidence=0.65,
        min_hand_presence_confidence=0.65,
        min_tracking_confidence=0.65,
    )
    controller = ActionController(dry_run=dry_run)

    capture = cv2.VideoCapture(camera_index)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open webcam at index {camera_index}.")

    started_at = monotonic()

    with vision.HandLandmarker.create_from_options(options) as landmarker:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int((monotonic() - started_at) * 1000)
            results = landmarker.detect_for_video(mp_image, timestamp_ms)
            gesture_name = "unknown"
            confidence = 0.0
            action_event = None

            if results.hand_landmarks:
                for index, hand_landmarks in enumerate(results.hand_landmarks):
                    handedness = "Right"
                    if results.handedness:
                        handedness = results.handedness[index][0].category_name

                    gesture = recognize_gesture(_to_landmarks(hand_landmarks), handedness)
                    gesture_name = gesture.name
                    confidence = gesture.confidence
                    action_event = controller.trigger(gesture.name)

                    _draw_landmarks(frame, hand_landmarks)

            _draw_status(frame, gesture_name, confidence, action_event)
            cv2.putText(
                frame,
                "Press Q to quit",
                (18, frame.shape[0] - 22),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (240, 240, 240),
                1,
                cv2.LINE_AA,
            )

            cv2.imshow("Syntecxhub Hand Gesture Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    capture.release()
    cv2.destroyAllWindows()


def parse_args() -> Tuple[int, bool, int, Path]:
    parser = argparse.ArgumentParser(description="Real-time hand gesture recognition demo.")
    parser.add_argument("--camera", type=int, default=0, help="Webcam index.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions on screen without sending keyboard shortcuts.",
    )
    parser.add_argument("--hands", type=int, default=1, help="Maximum number of hands.")
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path to the MediaPipe hand_landmarker.task model.",
    )
    args = parser.parse_args()
    return args.camera, args.dry_run, args.hands, args.model


def main() -> None:
    camera_index, dry_run, max_num_hands, model_path = parse_args()
    run_webcam_demo(
        camera_index=camera_index,
        dry_run=dry_run,
        max_num_hands=max_num_hands,
        model_path=model_path,
    )


if __name__ == "__main__":
    main()
