import importlib.util
import sys
from pathlib import Path

import pytest


def pytest_addoption(parser):
    parser.addoption("--calc-plugin-root", default=None)


@pytest.fixture
def plugin_root(request):
    value = request.config.getoption("--calc-plugin-root")
    return Path(value).resolve() if value else Path(__file__).resolve().parent


@pytest.fixture
def load_script(plugin_root):
    def load(relative):
        path = plugin_root / relative
        spec = importlib.util.spec_from_file_location("calc_fixture_module", path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    return load
