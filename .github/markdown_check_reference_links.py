import re
from pathlib import Path
from pprint import pprint
from subprocess import check_output


def check_path(path):
    bad_files = {}

    for file in tuple(Path(path).rglob("*.md")):
        file: Path
        with file.open() as f:
            html = check_output("pandoc", stdin=f, encoding="utf8")

        # pre
        html = re.sub(r"<pre.*?</pre>", "", html, flags=re.DOTALL)

        # pr
        html = re.sub(r'<p><a href="https://github.com/.*?/pull/\d+">\d+</a> .*?</p>', "", html)

        if m := re.findall(r"\[[^\[\]]+]\[[^\[\]]*]", html):
            bad_files[file.relative_to(path).as_posix()] = m

    return bad_files


if __name__ == "__main__":
    res = check_path("src/")
    pprint(res)
