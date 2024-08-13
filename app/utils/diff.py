from difflib import unified_diff


# https://docs.python.org/3/library/difflib.html#difflib.unified_diff
def get_diff(a: str, b: str) -> str:
    diff = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
    return "\n".join(list(diff))
