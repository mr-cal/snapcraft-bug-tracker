import argparse
import csv
from pathlib import Path
import requests
from dparse import parse, filetypes

"""Fetch craft library requirements for an application."""

CRAFT_LIBRARIES = {
    "craft-application",
    "craft-archives",
    "craft-cli",
    "craft-grammar",
    "craft-parts",
    "craft-providers",
    "craft-store",
}


def get_reqs(parsed_args: argparse.Namespace) -> None:
    """Fetch craft library requirements for an application."""
    user: str = parsed_args.user
    project: str = parsed_args.project
    branch: str = parsed_args.branch

    url = f"https://raw.githubusercontent.com/{user}/{project}/{branch}/requirements.txt"
    reqs_request = requests.get(url)

    if reqs_request.status_code != 200:
        raise RuntimeError(f"Could not fetch requirements.txt from {url}")

    df = parse(reqs_request.text, file_type=filetypes.requirements_txt)
    deps = {dep.name: dep.specs for dep in df.dependencies}

    # normalize the version and covert to string
    for dep, spec in deps.items():
        if not spec:
            deps[dep] = "unknown version"
        else:
            deps[dep] = str(spec).lstrip("=")

    # set version to "not found" for any missing deps
    for lib in CRAFT_LIBRARIES:
        if lib not in deps:
            deps[lib] = "not found"

    # write to data file
    with Path(f"data/{project}-deps.csv").open("w", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["library", "version"])
        for lib in CRAFT_LIBRARIES:
            writer.writerow([lib, deps[lib]])
