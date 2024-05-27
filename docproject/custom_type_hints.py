from typing import TypeVar, Generic

T = TypeVar("T")


class Bucket(Generic[T]):
    "Cloud storage bucket"
