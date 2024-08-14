from difflib import unified_diff


html_diff_template = open("app/utils/diff.html").read()


# https://docs.python.org/3/library/difflib.html#difflib.unified_diff
def get_diff(a: str, b: str) -> str:
    diff = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
    return "\n".join(list(diff))


def get_html_diff(a: str, b: str) -> str:
    diff = unified_diff(a.splitlines(), b.splitlines(), lineterm="")
    diff = "\n".join(list(diff))
    diff = diff.replace("`", "\`")
    return html_diff_template.replace("{{ diff }}", diff)
