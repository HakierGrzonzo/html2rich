from typing import List, TypeVar, Generator, Tuple


def split_array(array: List, predicate=lambda a: a is None):
    res = []
    for item in array:
        if predicate(item):
            yield res
            res = []
        else:
            res.append(item)
    if len(res) > 0:
        yield res


T = TypeVar("T")


def prev_current_next(
    iterable: List[T],
) -> Generator[Tuple[T | None, T, T | None], None, None]:
    padded = [None, *iterable, None]
    for i in range(1, len(iterable) + 1):
        yield padded[i - 1], padded[i], padded[i + 1]
