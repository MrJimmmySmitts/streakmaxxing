# StreakMaxxing

StreakMaxxing is a simple task streak management core that supports:

- Add Streak
- View Streaks (all streaks)
- View Streak by ID
- Add to Streak using customizable durations (days, weeks, hours, minutes)
- Reset Streak
- Notify users when a streak is close to expiration

## Quick start

```bash
python -m pip install -e .
pytest
```

## Core API

`StreakService` exposes:

- `add_streak(name, expiry_window)`
- `list_streaks()`
- `get_streak(streak_id)`
- `add_to_streak(streak_id, days=0, weeks=0, hours=0, minutes=0)`
- `reset_streak(streak_id)`
- `notify_expiring_streaks(window)`
