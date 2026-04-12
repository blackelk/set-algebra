"""
Reads README.md.
Extracts only fenced blocks opened with ```python.
Feeds each block to doctest.
Fails with a readable report if any example diverges.

What this catches:
    broken doctest examples
    wrong displayed output
    syntax errors inside ```python fences
    missing imports inside blocks

What it does not catch:
    malformed non-python code fences
    single-backtick markdown problems
    >>> appearing in prose outside fenced Python blocks
"""
from dataclasses import dataclass
import doctest
import pathlib
import re


README_PATH = pathlib.Path(__file__).resolve().parents[1] / "README.md"


@dataclass
class ReadmeBlock:
    index: int
    start_line: int
    code: str


def extract_python_fenced_blocks(text: str) -> list[ReadmeBlock]:
    """
    Extract fenced code blocks of the form:

    ```python
    ...
    ```

    Returns blocks with their starting line number in the README.
    """
    pattern = re.compile(
        r"^```python[ \t]*\n(.*?)^```[ \t]*$",
        re.MULTILINE | re.DOTALL,
    )
    blocks: list[ReadmeBlock] = []

    for index, match in enumerate(pattern.finditer(text), start=1):
        block_text = match.group(1)

        # Line number of the first code line inside the fence.
        start_line = text[: match.start(1)].count("\n") + 1

        blocks.append(
            ReadmeBlock(
                index = index,
                start_line = start_line,
                code = block_text,
            )
        )

    return blocks


def run_doctest_block(block: ReadmeBlock, *,
                      parser: doctest.DocTestParser,
                      runner: doctest.DocTestRunner,
                     ) -> tuple[int, int]:
    """
    Run one extracted block through doctest.

    Returns:
        (failures, attempts)
    """
    doctest_obj = parser.get_doctest(
        block.code,
        globs = {}, # Each block must import stuff it needs
        name = f"README.md:block_{block.index}",
        filename = str(README_PATH),
        lineno = block.start_line,
    )
    return runner.run(doctest_obj)


def test_readme_python_blocks() -> None:
    text = README_PATH.read_text(encoding = "utf-8")

    blocks = extract_python_fenced_blocks(text)
    assert blocks, f"No ```python fenced blocks found in {README_PATH}"

    parser = doctest.DocTestParser()

    runner = doctest.DocTestRunner(optionflags = doctest.ELLIPSIS)

    total_failures = 0
    total_attempts = 0

    for block in blocks:
        failures, attempts = run_doctest_block(
            block,
            parser = parser,
            runner = runner,
        )
        total_failures += failures
        total_attempts += attempts

    if total_failures:
        raise AssertionError(
            f"README doctest failures: {total_failures} failed out of {total_attempts} checks"
        )
