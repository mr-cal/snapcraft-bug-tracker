import argparse
import csv
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Union
import requests
import re
import string
from dparse import parse, filetypes


PACKAGE_LINE_REGEX = re.compile(r"^([A-Za-z0-9_.-]+)( *[~<>=!]==?)?(.*)")


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

    print(df.dependencies)

    #Jkcraft_providers = df.
