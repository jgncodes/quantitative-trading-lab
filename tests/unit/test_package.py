"smoke tests"

from importlib.metadata import version

import quantlab


def test_package_import() -> None:
    "verifies that the package can be imported"
    assert quantlab.__name__ == "quantlab"


def test_package_version() -> None:
    "verifies that the package has installed version metadata"
    assert version("quantitative-trading-lab")
