from typing import Callable, TypeVar
from typing_extensions import Concatenate, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")


def printing_decorator(func: Callable[P, T]) -> Callable[Concatenate[str, P], T]:
    def wrapper(msg: str, /, *args: P.args, **kwds: P.kwargs) -> T:
        print("Before calling:", func, "with", msg, "and", *args, **kwds)
        result = func(*args, **kwds)
        print(f"After calling: {result}")

        return result

    print("Called first.")
    return wrapper


@printing_decorator
def add_forty_two(value: int) -> int:
    return value + 42


if __name__ == "__main__":
    add_forty_two("two", 3)
