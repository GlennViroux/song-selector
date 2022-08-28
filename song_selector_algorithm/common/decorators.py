"""custom-made python decorators"""

import functools
import time
from typing import Optional

from common.logger import StuBruLogger


def log_exec_time(prefix: Optional[str]):
    """Decorator to log execution time of a python function."""

    def log_exec_time_decorator(func):
        @functools.wraps(func)
        def wrapper_log_exec_time(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            StuBruLogger().info(f"{prefix}{time.perf_counter() - start:.2f}s")

            return result

        return wrapper_log_exec_time

    return log_exec_time_decorator
