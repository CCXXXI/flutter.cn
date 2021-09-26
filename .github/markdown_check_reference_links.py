import re
from pathlib import Path
from subprocess import check_output
from sys import argv


def check_path(path):
    bad_files = []

    for file in tuple(Path(path).rglob("*.md")):
        file: Path
        with file.open() as f:
            html = check_output("pandoc", stdin=f, encoding="utf8")

        # pre
        html = re.sub(r"<pre.*?</pre>", "", html, flags=re.DOTALL)

        # pr
        html = re.sub(
            r'<p><a href="https://github.com/.*?/pull/\d+">\d+</a> .*?</p>', "", html
        )

        if re.search(r"\[[^\[\]]+]\[[^\[\]]*]", html):
            bad_files.append(file.relative_to(path).as_posix())

    return bad_files


if __name__ == "__main__":
    res = check_path('src/')
    print(*res, sep="\n")
