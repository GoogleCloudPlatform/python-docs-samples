#!/usr/bin/env python

# Copyright (C) 2023 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script to convert type hints to follow PEP-0585

For more information, see https://peps.python.org/pep-0585

To run from the repository's root directory:
    python convert-types.py
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
import difflib
from glob import glob
import logging
import re
import sys
from typing import NamedTuple, TypeVar

# Cases not covered:
# - Multi-line imports like `from M import (\nA,\nB,\n)`
# - Importing `typing` directly like `import typing` and `x: typing.Any`
# - Parsing types with `|` syntax like Union or Optional
# - typing.re.Match --> re.Match
# - typing.re.Pattern --> re.Pattern


BUILTIN_TYPES = {"Tuple", "List", "Dict", "Set", "FrozenSet", "Type"}
COLLECTIONS_TYPES = {"Deque", "DefaultDict", "OrderedDict", "Counter", "ChainMap"}
COLLECTIONS_ABC_TYPES = {
    "Awaitable",
    "Coroutine",
    "AsyncIterable",
    "AsyncIterator",
    "AsyncGenerator",
    "Iterable",
    "Iterator",
    "Generator",
    "Reversible",
    "Container",
    "Collection",
    "Callable",
    "AbstractSet",
    "MutableSet",
    "Mapping",
    "MutableMapping",
    "Sequence",
    "MutableSequence",
    "ByteString",
    "MappingView",
    "KeysView",
    "ItemsView",
    "ValuesView",
}
CONTEXTLIB_TYPES = {"ContextManager", "AsyncContextManager"}
RE_TYPES = {"Match", "Pattern"}

RENAME_TYPES = {
    "Tuple": "tuple",  # builtin
    "List": "list",  # builtin
    "Dict": "dict",  # builtin
    "Set": "set",  # builtin
    "FrozenSet": "frozenset",  # builtin
    "Type": "type",  # builtin
    "Deque": "deque",  # collections
    "DefaultDict": "defaultdict",  # collections
    "AbstractSet": "Set",  # collections.abc
    "ContextManager": "AbstractContextManager",  # contextlib
    "AsyncContextManager": "AbstractAsyncContextManager",  # contextlib
}

# Parser a = String -> (a, String)
a = TypeVar("a")
Parser = Callable[[str], tuple[a, str]]


class TypeHint(NamedTuple):
    name: str
    args: list[TypeHint]

    def __repr__(self) -> str:
        match (self.name, self.args):
            case ("Optional", [x]):
                return f"{x} | None"
            case ("Union", args):
                return " | ".join(map(str, args))
            case (name, []):
                return name
            case (name, args):
                return f"{name}[{', '.join(map(str, args))}]"

    def patch(self, types: set[str]) -> TypeHint:
        if self.name in types:
            name = RENAME_TYPES.get(self.name, self.name)
        else:
            name = self.name
        return TypeHint(name, [arg.patch(types) for arg in self.args])


def patch_file(file_path: str, dry_run: bool = False, quiet: bool = False) -> None:
    with open(file_path) as f:
        before = f.read()
    try:
        lines = [line.rstrip() for line in before.splitlines()]
        if types := find_typing_imports(lines):
            lines = insert_import_annotations(lines)
            lines = [patched for line in lines for patched in patch_imports(line)]
            lines = sort_imports(lines)
            after = patch_type_hints("\n".join(lines), types) + "\n"
            if not dry_run:
                if before != after:
                    with open(file_path, "w") as f:
                        f.write(after)
                    print(file_path)
            elif not quiet:
                print(f"| {file_path}")
                print(f"+--{'-' * len(file_path)}")
                diffs = difflib.context_diff(
                    before.splitlines(keepends=True),
                    after.splitlines(keepends=True),
                    fromfile="Before changes",
                    tofile="After changes",
                    n=1,
                )
                sys.stdout.writelines(diffs)
                print(f"+{'=' * 100}")
                print("| Press [ENTER] to continue to the next file")
                input()
    except Exception:
        logging.exception(f"Could not process file: {file_path}")


def insert_import_annotations(lines: list[str]) -> list[str]:
    new_import = "from __future__ import annotations"
    if new_import in lines:
        return lines

    match find_import(lines):
        case None:
            return lines
        case i:
            if lines[i].startswith("from __future__ import "):
                return lines[:i] + [new_import] + lines[i:]
            return lines[:i] + [new_import, ""] + lines[i:]


def find_typing_imports(lines: list[str]) -> set[str]:
    return {
        name.strip()
        for line in lines
        if line.startswith("from typing import ")
        for name in line.split("import")[1].split(",")
    }


def find_import(lines: list[str]) -> int | None:
    for i, line in enumerate(lines):
        if line.startswith(("import ", "from ")):
            return i
    return None


def get_imports_group(lines: list[str]) -> tuple[list[str], list[str]]:
    for i, line in enumerate(lines):
        if not line.strip() or line.startswith("#"):
            return (lines[:i], lines[i:])
    return ([], lines)


def import_name(line: str) -> str:
    match line.split():
        case ["import", name, *_]:
            return name
        case ["from", name, "import", *_]:
            return name
    raise ValueError(f"not an import: {line}")


def sort_imports(lines: list[str]) -> list[str]:
    match find_import(lines):
        case None:
            return lines
        case i:
            (imports, left) = get_imports_group(lines[i:])
            if imports:
                return lines[:i] + sorted(imports, key=import_name) + sort_imports(left)
            return left


def patch_imports(line: str) -> Iterator[str]:
    if not line.startswith("from typing import "):
        yield line
        return

    types = find_typing_imports([line])
    collections_types = types.intersection(COLLECTIONS_TYPES)
    collections_abc_types = types.intersection(COLLECTIONS_ABC_TYPES)
    contextlib_types = types.intersection(CONTEXTLIB_TYPES)
    re_types = types.intersection(RE_TYPES)
    typing_types = (
        types
        - BUILTIN_TYPES
        - COLLECTIONS_TYPES
        - COLLECTIONS_ABC_TYPES
        - CONTEXTLIB_TYPES
        - RE_TYPES
        - {"Optional", "Union"}
    )

    rename = lambda name: RENAME_TYPES.get(name, name)
    if collections_types:
        names = sorted(map(rename, collections_types))
        yield f"from collections import {', '.join(names)}"
    if collections_abc_types:
        names = sorted(map(rename, collections_abc_types))
        yield f"from collections.abc import {', '.join(names)}"
    if contextlib_types:
        names = sorted(map(rename, contextlib_types))
        yield f"from contextlib import {', '.join(names)}"
    if re_types:
        names = sorted(map(rename, re_types))
        yield f"from re import {', '.join(names)}"
    if typing_types:
        names = sorted(map(rename, typing_types))
        yield f"from typing import {', '.join(names)}"


def patch_type_hints(txt: str, types: set[str]) -> str:
    if m := re.search(rf"(?:->|:) *(\w+)", txt):
        (typ, left) = parse_type_hint(txt[m.start(1) :])
        return f"{txt[:m.start(1)]}{typ.patch(types)}{patch_type_hints(left, types)}"
    return txt


# Parser combinators
def parse_text(src: str, txt: str) -> tuple[str, str]:
    if src.startswith(txt):
        return (src[: len(txt)], src[len(txt) :])
    raise SyntaxError("text")


def parse_identifier(src: str) -> tuple[str, str]:
    if m := re.search(r"[\w\._]+", src):
        return (m.group(), src[m.end() :])
    raise SyntaxError("name")


def parse_zero_or_more(src: str, parser: Parser[a]) -> tuple[list[a], str]:
    try:
        (x, src) = parser(src)
        (xs, src) = parse_zero_or_more(src, parser)
        return ([x] + xs, src)
    except SyntaxError:
        return ([], src)


def parse_comma_separated(src: str, parser: Parser[a]) -> tuple[list[a], str]:
    def parse_next(src: str) -> tuple[a, str]:
        (_, src) = parse_text(src, ",")
        (_, src) = parse_zero_or_more(src, lambda src: parse_text(src, " "))
        return parser(src)

    try:
        (x, src) = parser(src)
        (xs, src) = parse_zero_or_more(src, parse_next)
        return ([x] + xs, src)
    except SyntaxError:
        return ([], src)


def parse_type_hint(src: str) -> tuple[TypeHint, str]:
    (name, src) = parse_identifier(src)
    try:
        (_, src) = parse_text(src, "[")
        (args, src) = parse_comma_separated(src, parse_type_hint)
        (_, src) = parse_text(src, "]")
        return (TypeHint(name, args), src)
    except SyntaxError:
        return (TypeHint(name, []), src)


def run(patterns: list[str], dry_run: bool = False, quiet: bool = False):
    for pattern in patterns:
        for filename in glob(pattern):
            patch_file(filename, dry_run, quiet)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("patterns", nargs="*", default=["**/*.py"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    run(**args.__dict__)
