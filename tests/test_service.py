from datetime import datetime, timedelta, timezone

import pytest

from streakmaxxing.service import StreakService


def test_add_and_list_and_get_streak() -> None:
    service = StreakService()

    streak = service.add_streak("Workout", timedelta(days=2))

    assert service.list_streaks() == [streak]
    assert service.get_streak(streak.id).name == "Workout"


def test_add_to_streak_adds_expiry_window() -> None:
    service = StreakService()
    streak = service.add_streak("Reading", timedelta(days=1))

    updated = service.add_to_streak(streak.id)

    assert updated.value == timedelta(days=1)


def test_reset_streak() -> None:
    service = StreakService()
    streak = service.add_streak("No sugar", timedelta(days=3))
    for _ in range(6):
        service.add_to_streak(streak.id)

    reset = service.reset_streak(streak.id)

    assert reset.value == timedelta(0)


def test_notify_user_of_streak_expiration() -> None:
    service = StreakService()
    streak = service.add_streak("Hydration", timedelta(hours=12))

    base_time = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
    service.add_to_streak(streak.id, now=base_time)

    notifications = service.notify_expiring_streaks(
        window=timedelta(hours=2),
        now=base_time + timedelta(hours=10, minutes=30),
    )

    assert len(notifications) == 1
    assert notifications[0]["streak_id"] == streak.id


def test_notify_ignores_non_expiring_streaks() -> None:
    service = StreakService()
    streak = service.add_streak("Meditation", timedelta(days=2))
    now = datetime(2026, 1, 1, 10, tzinfo=timezone.utc)
    service.add_to_streak(streak.id, now=now)

    notifications = service.notify_expiring_streaks(
        window=timedelta(hours=1),
        now=now + timedelta(hours=10),
    )

    assert notifications == []


def test_validation_errors() -> None:
    service = StreakService()
    with pytest.raises(ValueError):
        service.add_streak("", timedelta(days=1))

