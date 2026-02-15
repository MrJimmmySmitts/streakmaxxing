from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4


@dataclass
class Streak:
    """A single streak tracked by the system."""

    name: str
    expiry_window: timedelta
    id: str = field(default_factory=lambda: str(uuid4()))
    value: timedelta = field(default_factory=timedelta)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    notify_before: timedelta = field(default_factory=lambda: timedelta(hours=2))

    def __post_init__(self) -> None:
        if self.notify_before <= timedelta(0):
            raise ValueError("notify_before must be positive")

    def add_time(self, amount: timedelta, now: datetime | None = None) -> None:
        """Add arbitrary time to the streak and refresh its update timestamp."""
        if amount <= timedelta(0):
            raise ValueError("amount must be positive")
        at_time = now or datetime.now(timezone.utc)
        self.value += amount
        self.last_updated_at = at_time

    def reset(self, now: datetime | None = None) -> None:
        """Reset streak value to zero."""
        at_time = now or datetime.now(timezone.utc)
        self.value = timedelta(0)
        self.last_updated_at = at_time

    def expires_at(self) -> datetime:
        """Return when the streak is considered expired if not updated."""
        return self.last_updated_at + self.expiry_window

    def is_expiring_within(self, window: timedelta, now: datetime | None = None) -> bool:
        """Return True when streak expires within the given window."""
        if window < timedelta(0):
            raise ValueError("window cannot be negative")
        at_time = now or datetime.now(timezone.utc)
        time_to_expiry = self.expires_at() - at_time
        return timedelta(0) <= time_to_expiry <= window
