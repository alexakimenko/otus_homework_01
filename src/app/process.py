import datetime
import gzip
import os
import re
from string import Template

import structlog
import yaml  # type: ignore

from .utils import LogFile, configure_logging

logger = structlog.get_logger()
configure_logging()


def load_config(config_path):
    if not os.path.exists(config_path):
        logger.error("Config file is not found", config_path=config_path)
        raise FileNotFoundError(f"Config file {config_path} is not found")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def find_latest_log(log_dir):
    log_files = []

    log_pattern = re.compile(r"nginx-access-ui\.log-(\d{8})\.*")

    for f in os.listdir(log_dir):
        match = log_pattern.match(f)
        if match:
            date_str = match.group(1)
            date = datetime.datetime.strptime(date_str, "%Y%m%d")
            log_files.append(LogFile(path=os.path.join(log_dir, f), date=date))

    if not log_files:
        logger.error("No logs available for processing", log_dir=log_dir)
        raise FileNotFoundError("No logs available for processing.")

    latest_log = max(log_files, key=lambda log: log.date)
    return latest_log


def parse_log(log_path):
    url_data = {}
    is_gzipped = log_path.endswith(".gz")
    open_func = gzip.open if is_gzipped else open
    try:
        with open_func(log_path, "rt", encoding="utf-8") as log_file:
            for line in log_file:
                try:
                    data = line.split(" ")
                    url = data[7]
                    request_time = float(data[-1])
                    if url not in url_data:
                        url_data[url] = {"count": 0, "time_sum": 0.0, "time_max": 0.0}
                    url_data[url]["count"] += 1
                    url_data[url]["time_sum"] += request_time
                    if request_time > url_data[url]["time_max"]:
                        url_data[url]["time_max"] = request_time
                except (IndexError, ValueError):
                    logger.warning("Line parsing error", line=line)
                    continue
    except Exception as e:
        logger.error(
            "Failed to open or process log file", log_path=log_path, error=str(e)
        )
        raise
    return url_data


def generate_report(url_data, report_path, template_path, tablesorter_js, report_size):
    url_stats = sorted(url_data.items(), key=lambda x: x[1]["time_sum"], reverse=True)[
        :report_size
    ]
    report_data = []
    for url, data in url_stats:
        data["url"] = url
        data["time_avg"] = data["time_sum"] / data["count"]
        report_data.append(data)

    table_json = str(report_data)

    try:
        with open(template_path, "r") as f:
            template_content = f.read()

        template = Template(template_content)
        report_content = template.safe_substitute(
            table_json=table_json, js_path=tablesorter_js
        )

        with open(report_path, "w") as f:
            f.write(report_content)
        logger.info("Report generated successfully", report_path=report_path)
    except Exception as e:
        logger.error("Failed to generate report", report_path=report_path, error=str(e))
        raise


def main(config_path):
    config = load_config(config_path)
    logger.info("loaded config", config=config)
    latest_log = find_latest_log(config["log_dir"])
    url_data = parse_log(latest_log.path)

    report_date = latest_log.date.strftime("%Y.%m.%d")
    report_name = f"report-{report_date}.html"
    report_path = os.path.join(config["report_dir"], report_name)

    generate_report(
        url_data,
        report_path,
        config["report_template"],
        config["tablesorter_js"],
        config["report_size"],
    )
