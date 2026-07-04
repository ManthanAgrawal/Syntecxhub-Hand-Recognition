import unittest

from gesture_control.gestures import Landmark, classify_fingers, recognize_gesture


def make_hand(extended):
    points = [Landmark(0.5, 0.8) for _ in range(21)]

    points[0] = Landmark(0.5, 0.9)
    points[2] = Landmark(0.42, 0.72)
    points[3] = Landmark(0.36, 0.68)
    points[4] = Landmark(0.30 if extended.get("thumb") else 0.45, 0.62)

    finger_pairs = {
        "index": (6, 8, 0.42),
        "middle": (10, 12, 0.50),
        "ring": (14, 16, 0.58),
        "pinky": (18, 20, 0.66),
    }
    for finger, (pip, tip, x) in finger_pairs.items():
        points[pip] = Landmark(x, 0.55)
        points[tip] = Landmark(x, 0.35 if extended.get(finger) else 0.66)

    return points


class GestureRecognitionTests(unittest.TestCase):
    def test_open_palm(self):
        hand = make_hand(
            {"thumb": True, "index": True, "middle": True, "ring": True, "pinky": True}
        )
        self.assertEqual(recognize_gesture(hand).name, "open_palm")

    def test_fist(self):
        self.assertEqual(recognize_gesture(make_hand({})).name, "fist")

    def test_thumbs_up(self):
        hand = make_hand({"thumb": True})
        hand[4] = Landmark(0.30, 0.55)
        self.assertEqual(recognize_gesture(hand).name, "thumbs_up")

    def test_peace(self):
        hand = make_hand({"index": True, "middle": True})
        self.assertEqual(recognize_gesture(hand).name, "peace")

    def test_point(self):
        hand = make_hand({"index": True})
        self.assertEqual(recognize_gesture(hand).name, "point")

    def test_finger_classifier_returns_all_fingers(self):
        hand = make_hand({"index": True})
        self.assertEqual(
            set(classify_fingers(hand).keys()),
            {"thumb", "index", "middle", "ring", "pinky"},
        )


if __name__ == "__main__":
    unittest.main()
