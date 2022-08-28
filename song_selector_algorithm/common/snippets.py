"""independent code snippets"""

from datetime import timedelta


def pretty_duration(delta: timedelta) -> str:
    """Print a timedelta in a user-friendly format."""

    seconds = delta.total_seconds() - (days := delta.days) * 24 * 3600
    seconds = seconds - (hours := seconds // 3600) * 3600
    seconds = seconds - (minutes := seconds // 60) * 60

    result = []
    if days:
        result.append(f"{int(days)} day{'s' if int(days) > 1 else ''}")
    if hours:
        result.append(f"{int(hours)}h")
    if minutes:
        result.append(f"{int(minutes)}min")
    if seconds:
        result.append(f"{int(seconds)}sec")

    if not result:
        return "0sec"
    if len(result) == 1:
        return result[0]

    return ", ".join(result[:-1]) + f" and {result[-1]}"
