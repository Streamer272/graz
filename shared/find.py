from typing import Callable, Any, List


def find(array: List[Any], function: Callable):
    for item in array:
        if function(item):
            return item
    raise Exception("Item not found")
