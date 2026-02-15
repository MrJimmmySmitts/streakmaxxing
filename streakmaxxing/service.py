from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta, timezone

from .models import Streak


class StreakService:
    """In-memory service that implements StreakMaxxing requirements."""

    def __init__(self) -> None:
        self._streaks: dict[str, Streak] = {}

    def add_streak(self, name: str, expiry_window: timedelta) -> Streak:
        """Create and register a new streak."""
        if not name.strip():
            raise ValueError("name is required")
        if expiry_window <= timedelta(0):
            raise ValueError("expiry_window must be positive")

        streak = Streak(name=name.strip(), expiry_window=expiry_window)
        self._streaks[streak.id] = streak
        return streak

    def list_streaks(self) -> list[Streak]:
        """View all streaks."""
        return list(self._streaks.values())

    def get_streak(self, streak_id: str) -> Streak:
        """View one streak by id."""
        try:
            return self._streaks[streak_id]
        except KeyError as exc:
            raise KeyError(f"streak not found: {streak_id}") from exc

    def add_to_streak(
        self,
        streak_id: str,
        *,
        days: int = 0,
        weeks: int = 0,
        hours: int = 0,
        minutes: int = 0,
        now: datetime | None = None,
    ) -> Streak:
        """Add custom duration to streak."""
        amount = timedelta(days=days, weeks=weeks, hours=hours, minutes=minutes)
        streak = self.get_streak(streak_id)
        streak.add_time(amount, now=now)
        return streak

    def reset_streak(self, streak_id: str, now: datetime | None = None) -> Streak:
        """Reset a streak to zero."""
        streak = self.get_streak(streak_id)
        streak.reset(now=now)
        return streak

    def notify_expiring_streaks(
        self,
        window: timedelta,
        now: datetime | None = None,
    ) -> list[dict[str, str]]:
        """Find streaks close to expiry and build simple notifications."""
        at_time = now or datetime.now(timezone.utc)
        notifications: list[dict[str, str]] = []
        for streak in self._streaks.values():
            if streak.is_expiring_within(window, now=at_time):
                notifications.append(
                    {
                        "streak_id": streak.id,
                        "title": f"Streak '{streak.name}' is about to expire",
                        "message": (
                            f"Your streak expires at {streak.expires_at().isoformat()}. "
                            "Add time to keep it alive."
                        ),
                    }
                )
        return notifications

    def export(self) -> list[dict]:
        """Return serializable representation of all streaks."""
        payload = []
        for streak in self._streaks.values():
            item = asdict(streak)
            item["expiry_window"] = int(streak.expiry_window.total_seconds())
            item["value"] = int(streak.value.total_seconds())
            item["created_at"] = streak.created_at.isoformat()
            item["last_updated_at"] = streak.last_updated_at.isoformat()
            payload.append(item)
        return payload
