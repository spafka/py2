from typing import List, Callable, TypeVar

T = TypeVar('T')
V = TypeVar('V')


def apply_to_each(func: Callable[[T], V], lst: List[T]) -> List[V]:
    return [func(item) for item in lst]


def double(x: int) -> str:
    return str(x * 2)


numbers: List[int] = [1, 2, 3, 4]
doubled_numbers: List[str] = apply_to_each(double, numbers)

print(doubled_numbers)  # 输出: [2, 4, 6, 8]
