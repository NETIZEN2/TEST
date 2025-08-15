"""Minimal FastAPI stub for tests when real dependency is absent."""
from typing import Callable, Dict, Tuple


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class FastAPI:
    def __init__(self) -> None:
        self.routes: Dict[Tuple[str, str], Callable] = {}

    def get(self, path: str, **_: object) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[(path, "GET")] = func
            return func

        return decorator

    def post(self, path: str, **_: object) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[(path, "POST")] = func
            return func

        return decorator
