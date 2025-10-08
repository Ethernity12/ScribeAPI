import inspect
import logging
import functools
import time
from pathlib import Path


def setup_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(Path('logs', name + '.log'), encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


class DBOperationLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
    def __call__(self, func):
        is_async = inspect.iscoroutinefunction(func)
        func_name = func.__name__

        if is_async:
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.perf_counter()
                self.logger.info(f"🟢 Start async: {func_name}")
                try:
                    result = await func(*args, **kwargs)
                    elapsed = (time.perf_counter() - start) * 1000
                    self.logger.info(f"✅ Done {func_name} ({elapsed:.2f} ms)")
                    return result
                except Exception as e:
                    self.logger.error(f"❌ Error in {func_name}: {e}")
                    raise
            return async_wrapper

        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.perf_counter()
                self.logger.info(f"🟢 Start sync: {func_name}")
                try:
                    result = func(*args, **kwargs)
                    elapsed = (time.perf_counter() - start) * 1000
                    self.logger.info(f"✅ Done {func_name} ({elapsed:.2f} ms)")
                    return result
                except Exception as e:
                    self.logger.error(f"❌ Error in {func_name}: {e}")
                    raise
            return sync_wrapper
        
        