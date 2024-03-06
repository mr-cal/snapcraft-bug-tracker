import argparse
import csv
from dataclasses import dataclass
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


@dataclass(frozen=True)
class CraftApplication():
    """TODO."""

    name: str
    branch: str = "main"
    owner: str = "canonical"


CRAFT_APPLICATIONS = {
    CraftApplication("charmcraft"),
    CraftApplication("rockcraft"),
    CraftApplication("snapcraft"),
}


def get_reqs(parsed_args: argparse.Namespace) -> None:
    """Fetch craft library requirements for all applications."""
    app_reqs: dict = {}
    for app in CRAFT_APPLICATIONS:
        app_reqs[app] = _get_reqs_for_project(app)

    # write to data file
    with Path("data/app-deps.csv").open("w", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        # TODO: programatically generate header
        writer.writerow(["library", "snapcraft", "rockcraft", "charmcraft"])
        for library in CRAFT_LIBRARIES:
            writer.writerow(
                [
                    library,
                    # TODO: programatically generate data
                    app_reqs[CraftApplication("snapcraft")][library],
                    app_reqs[CraftApplication("rockcraft")][library],
                    app_reqs[CraftApplication("charmcraft")][library]]
            )


def _get_reqs_for_project(app: CraftApplication) -> dict:
    """Fetch craft library requirements for an application."""
    url = f"https://raw.githubusercontent.com/{app.owner}/{app.name}/{app.branch}/requirements.txt"
    reqs_request = requests.get(url)

    if reqs_request.status_code != 200:
        raise RuntimeError(f"Could not fetch requirements.txt from {url}")

    df = parse(reqs_request.text, file_type=filetypes.requirements_txt)
    deps = {dep.name: dep.specs for dep in df.dependencies}

    # normalize the version and covert to string
    for dep, spec in deps.items():
        deps[dep] = str(spec).lstrip("=") if spec else "unknown"

    # only return craft library deps
    return {lib: deps.get(lib, "n/a") for lib in CRAFT_LIBRARIES}
