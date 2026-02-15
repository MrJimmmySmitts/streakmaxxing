# StreakMaxxing

StreakMaxxing is a simple task streak management core that supports:

- Add Streak
- View Streaks (all streaks)
- View Streak by ID
- Add to Streak (one click adds one expiry-window unit)
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
- `add_to_streak(streak_id)`
- `reset_streak(streak_id)`
- `notify_expiring_streaks(window)`


## Front-end (simple modern UI)

A lightweight static front-end is available at `frontend/index.html`.

Run it locally:

```bash
cd frontend
python -m http.server 8000
```

Then open <http://localhost:8000>.
