from dataclasses import dataclass
from time import monotonic
from typing import Dict, Optional


@dataclass(frozen=True)
class ActionEvent:
    gesture: str
    action: str
    status: str


class ActionController:
    """Maps recognized gestures to demo actions with a cooldown."""

    DEFAULT_ACTIONS: Dict[str, str] = {
        "open_palm": "play_pause",
        "fist": "mute",
        "thumbs_up": "volume_up",
        "peace": "volume_down",
        "point": "screenshot",
    }

    def __init__(self, cooldown_seconds: float = 1.2, dry_run: bool = False) -> None:
        self.cooldown_seconds = cooldown_seconds
        self.dry_run = dry_run
        self._last_action_at = 0.0
        self._keyboard = None

    def trigger(self, gesture: str) -> Optional[ActionEvent]:
        action = self.DEFAULT_ACTIONS.get(gesture)
        if not action:
            return None

        now = monotonic()
        if now - self._last_action_at < self.cooldown_seconds:
            return ActionEvent(gesture, action, "cooldown")

        self._last_action_at = now

        if self.dry_run:
            return ActionEvent(gesture, action, "preview")

        return self._execute(gesture, action)

    def _execute(self, gesture: str, action: str) -> ActionEvent:
        try:
            keyboard = self._load_keyboard()
            if action == "play_pause":
                keyboard.press("playpause")
            elif action == "mute":
                keyboard.press("volumemute")
            elif action == "volume_up":
                keyboard.press("volumeup")
            elif action == "volume_down":
                keyboard.press("volumedown")
            elif action == "screenshot":
                keyboard.press_and_release("windows+print screen")
            return ActionEvent(gesture, action, "sent")
        except Exception as exc:
            return ActionEvent(gesture, action, f"unavailable: {exc}")

    def _load_keyboard(self):
        if self._keyboard is None:
            import keyboard

            self._keyboard = keyboard
        return self._keyboard
