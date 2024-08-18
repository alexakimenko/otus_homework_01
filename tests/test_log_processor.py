import os
import tempfile

import pytest

from src.app.process import find_latest_log, load_config

config_yaml = """
log_dir: './logs'
report_dir: './reports'
report_size: 10
tablesorter_js: './jquery.tablesorter.min.js'
report_template: './report.html'
"""


@pytest.fixture
def config():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp:
        tmp.write(config_yaml.encode("utf-8"))
        tmp.flush()
        yield tmp.name
        os.remove(tmp.name)


def test_load_config(config):
    config_data = load_config(config)
    assert config_data["log_dir"] == "./logs"
    assert config_data["report_size"] == 10


def test_find_latest_log():
    with tempfile.TemporaryDirectory() as tmpdirname:
        log1 = os.path.join(tmpdirname, "nginx-access-ui.log-20230801")
        log2 = os.path.join(tmpdirname, "nginx-access-ui.log-20230802")
        with open(log1, "w") as f:
            f.write("")
        with open(log2, "w") as f:
            f.write("")

        latest_log = find_latest_log(tmpdirname)
        assert latest_log.path == log2
