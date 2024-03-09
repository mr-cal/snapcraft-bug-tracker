import sys

import starcraft_stats

"""Smoketests."""


def test_main(mocker):
    mocker.patch.object(
        sys,
        "argv",
        ["starcraft-stats", "fetch-reqs", "canonical", "snapcraft", "main"],
    )

    starcraft_stats.cli.main()
