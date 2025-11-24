"""Collection iteration transformations."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from functools import reduce
from itertools import cycle, islice, tee
from typing import Any, TypeVar, overload
import copy

from extended_data_types.transformations.core import Transform


T = TypeVar("T")
U = TypeVar("U")


def chain_iterators(*iterables: Iterable[T]) -> Iterator[T]:
    """Legacy helper to chain iterables."""
    for iterable in iterables:
        yield from iterable


def consume_iterator(iterator: Iterator[T], n: int | None = None) -> None:
    """Legacy helper to exhaust an iterator or a limited number of items."""
    if n is not None and n < 0:
        raise ValueError("n must be non-negative")
    if n is None:
        for _ in iterator:
            pass
        return
    for _ in range(n):
        try:
            next(iterator)
        except StopIteration:
            break


def cycle_iterator(iterable: Iterable[T], n: int | None = None) -> Iterator[T]:
    """Legacy helper to cycle over iterable, optionally a fixed number of cycles."""
    if n is not None and n < 0:
        raise ValueError("n must be non-negative")
    def _gen() -> Iterator[T]:
        if n is None:
            yield from cycle(iterable)
            return
        for _ in range(n):
            for item in iterable:
                yield item
    return _gen()


@overload
def peek_iterator(iterator: Iterator[T]) -> T | None: ...


@overload
def peek_iterator(iterator: Iterator[T], n: int) -> list[T] | None: ...


def peek_iterator(iterator: Iterator[T], n: int | None = None) -> T | list[T] | None:
    """Peek items without consuming the original iterator."""
    if n is not None and n < 0:
        raise ValueError("n must be non-negative")
    count = 1 if n is None else n
    duplicate = copy.copy(iterator)
    peeked = list(islice(duplicate, count))
    if not peeked:
        return None
    return peeked[0] if n is None else peeked


def skip_iterator(iterator: Iterator[T], count: int) -> Iterator[T]:
    """Skip first N elements of an iterator."""
    if count < 0:
        raise ValueError("count must be non-negative")
    for _ in range(count):
        try:
            next(iterator)
        except StopIteration:
            return iter(())
    return iterator


def take_iterator(iterator: Iterator[T], count: int) -> list[T]:
    """Take first N elements from an iterator."""
    if count < 0:
        raise ValueError("count must be non-negative")
    result: list[T] = []
    for _ in range(count):
        try:
            result.append(next(iterator))
        except StopIteration:
            break
    return result


def batch_iterate(items: Sequence[T], batch_size: int) -> Iterator[list[T]]:
    """Iterate over sequence in batches.

    Args:
        items: Sequence to iterate
        batch_size: Size of each batch

    Yields:
        Batches of items

    Example:
        >>> list(batch_iterate([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    for i in range(0, len(items), batch_size):
        yield list(items[i : i + batch_size])


def window_iterate(
    items: Sequence[T], window_size: int, step: int = 1
) -> Iterator[list[T]]:
    """Iterate over sliding windows of sequence.

    Args:
        items: Sequence to iterate
        window_size: Size of window
        step: Steps between windows

    Yields:
        Windows of items

    Example:
        >>> list(window_iterate([1, 2, 3, 4], 2))
        [[1, 2], [2, 3], [3, 4]]
        >>> list(window_iterate([1, 2, 3, 4], 2, 2))
        [[1, 2], [3, 4]]
    """
    for i in range(0, len(items) - window_size + 1, step):
        yield list(items[i : i + window_size])


def recursive_iterate(
    obj: Any, predicate: Callable[[Any], bool] | None = None
) -> Iterator[Any]:
    """Recursively iterate over nested structure.

    Args:
        obj: Object to iterate
        predicate: Optional filter for values

    Yields:
        Values from structure

    Example:
        >>> list(recursive_iterate({'a': [1, {'b': 2}]}))
        [1, 2]
        >>> list(recursive_iterate({'a': [1, {'b': 2}]}, lambda x: isinstance(x, int)))
        [1, 2]
    """
    if isinstance(obj, (dict, benedict)):
        yield from recursive_iterate(list(obj.values()), predicate)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            if isinstance(item, (dict, list, tuple, benedict)):
                yield from recursive_iterate(item, predicate)
            elif predicate is None or predicate(item):
                yield item
    elif predicate is None or predicate(obj):
        yield obj


def pairwise_iterate(items: Sequence[T]) -> Iterator[tuple[T, T]]:
    """Iterate over consecutive pairs.

    Args:
        items: Sequence to iterate

    Yields:
        Consecutive pairs of items

    Example:
        >>> list(pairwise_iterate([1, 2, 3, 4]))
        [(1, 2), (2, 3), (3, 4)]
    """
    for i in range(len(items) - 1):
        yield (items[i], items[i + 1])


def map_values(
    items: Sequence[T] | Mapping[Any, T], transform: Callable[[T], U]
) -> list[U] | dict[Any, U]:
    """Apply function to each value.

    Args:
        items: Sequence or mapping to transform
        transform: Function to apply

    Returns:
        Transformed sequence or mapping

    Example:
        >>> map_values([1, 2, 3], lambda x: x * 2)
        [2, 4, 6]
        >>> map_values({'a': 1, 'b': 2}, lambda x: x * 2)
        {'a': 2, 'b': 4}
    """
    if isinstance(items, Mapping):
        return {k: transform(v) for k, v in items.items()}
    return [transform(x) for x in items]


def filter_values(
    items: Sequence[T] | Mapping[Any, T], predicate: Callable[[T], bool]
) -> list[T] | dict[Any, T]:
    """Filter values by predicate.

    Args:
        items: Sequence or mapping to filter
        predicate: Function returning True for values to keep

    Returns:
        Filtered sequence or mapping

    Example:
        >>> filter_values([1, 2, 3, 4], lambda x: x % 2 == 0)
        [2, 4]
        >>> filter_values({'a': 1, 'b': 2}, lambda x: x > 1)
        {'b': 2}
    """
    if isinstance(items, Mapping):
        return {k: v for k, v in items.items() if predicate(v)}
    return [x for x in items if predicate(x)]


def reduce_values(items: Iterable[T], reducer: Callable[[U, T], U], initial: U) -> U:
    """Reduce sequence to single value.

    Args:
        items: Sequence to reduce
        reducer: Function to combine values
        initial: Initial value

    Returns:
        Reduced value

    Example:
        >>> reduce_values([1, 2, 3], lambda acc, x: acc + x, 0)
        6
    """
    return reduce(reducer, items, initial)


def find_value(
    items: Sequence[T] | Mapping[Any, T],
    predicate: Callable[[T], bool],
    default: T | None = None,
) -> T | None:
    """Find first value matching predicate.

    Args:
        items: Sequence or mapping to search
        predicate: Function returning True for match
        default: Value to return if no match

    Returns:
        Matching value or default

    Example:
        >>> find_value([1, 2, 3], lambda x: x > 2)
        3
        >>> find_value({'a': 1, 'b': 2}, lambda x: x > 5)
        None
    """
    values = items.values() if isinstance(items, Mapping) else items
    return next((x for x in values if predicate(x)), default)


def all_match(
    items: Sequence[T] | Mapping[Any, T], predicate: Callable[[T], bool]
) -> bool:
    """Check if all values match predicate.

    Args:
        items: Sequence or mapping to check
        predicate: Function to test values

    Returns:
        True if all values match

    Example:
        >>> all_match([2, 4, 6], lambda x: x % 2 == 0)
        True
    """
    values = items.values() if isinstance(items, Mapping) else items
    return all(predicate(x) for x in values)


def any_match(
    items: Sequence[T] | Mapping[Any, T], predicate: Callable[[T], bool]
) -> bool:
    """Check if any value matches predicate.

    Args:
        items: Sequence or mapping to check
        predicate: Function to test values

    Returns:
        True if any value matches

    Example:
        >>> any_match([1, 2, 3], lambda x: x > 2)
        True
    """
    values = items.values() if isinstance(items, Mapping) else items
    return any(predicate(x) for x in values)


# Register transforms
batch_iterate_transform = Transform(batch_iterate)
window_iterate_transform = Transform(window_iterate)
recursive_iterate_transform = Transform(recursive_iterate)
pairwise_iterate_transform = Transform(pairwise_iterate)
map_values_transform = Transform(map_values)
filter_values_transform = Transform(filter_values)
reduce_values_transform = Transform(reduce_values)
find_value_transform = Transform(find_value)
all_match_transform = Transform(all_match)
any_match_transform = Transform(any_match)
