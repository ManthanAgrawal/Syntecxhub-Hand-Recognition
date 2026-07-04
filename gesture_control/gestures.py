from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class Landmark:
    """Normalized landmark point returned by MediaPipe Hands."""

    x: float
    y: float
    z: float = 0.0


@dataclass(frozen=True)
class GestureResult:
    name: str
    confidence: float
    fingers: Dict[str, bool]


FINGER_TIPS = {
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20,
}

FINGER_PIPS = {
    "index": 6,
    "middle": 10,
    "ring": 14,
    "pinky": 18,
}


def _as_landmark_list(landmarks: Iterable[Landmark]) -> List[Landmark]:
    points = list(landmarks)
    if len(points) != 21:
        raise ValueError("MediaPipe Hands returns exactly 21 landmarks per hand.")
    return points


def _is_thumb_extended(points: List[Landmark], handedness: str) -> bool:
    thumb_tip = points[FINGER_TIPS["thumb"]]
    thumb_ip = points[3]
    thumb_mcp = points[2]

    if handedness.lower().startswith("left"):
        return thumb_tip.x > thumb_ip.x > thumb_mcp.x
    return thumb_tip.x < thumb_ip.x < thumb_mcp.x


def classify_fingers(
    landmarks: Iterable[Landmark], handedness: str = "Right"
) -> Dict[str, bool]:
    points = _as_landmark_list(landmarks)
    fingers = {"thumb": _is_thumb_extended(points, handedness)}

    for finger, tip_index in FINGER_TIPS.items():
        if finger == "thumb":
            continue
        pip_index = FINGER_PIPS[finger]
        fingers[finger] = points[tip_index].y < points[pip_index].y

    return fingers


def recognize_gesture(
    landmarks: Iterable[Landmark], handedness: str = "Right"
) -> GestureResult:
    """Classify a simple hand gesture from 21 normalized landmarks."""

    points = _as_landmark_list(landmarks)
    fingers = classify_fingers(points, handedness)
    extended_count = sum(fingers.values())

    thumb_tip = points[FINGER_TIPS["thumb"]]
    wrist = points[0]
    non_thumb_folded = not any(
        fingers[finger] for finger in ("index", "middle", "ring", "pinky")
    )
    thumb_is_vertical = thumb_tip.y < wrist.y - 0.12

    if all(fingers.values()):
        return GestureResult("open_palm", 0.96, fingers)

    if extended_count == 0:
        return GestureResult("fist", 0.94, fingers)

    if fingers["thumb"] and non_thumb_folded and thumb_is_vertical:
        return GestureResult("thumbs_up", 0.91, fingers)

    if (
        fingers["index"]
        and fingers["middle"]
        and not fingers["ring"]
        and not fingers["pinky"]
    ):
        return GestureResult("peace", 0.89, fingers)

    if fingers["index"] and extended_count == 1:
        return GestureResult("point", 0.88, fingers)

    return GestureResult("unknown", 0.45, fingers)


def gesture_label(name: Optional[str]) -> str:
    labels = {
        "open_palm": "Open Palm",
        "fist": "Fist",
        "thumbs_up": "Thumbs Up",
        "peace": "Peace",
        "point": "Point",
        "unknown": "Unknown",
    }
    return labels.get(name or "unknown", "Unknown")
