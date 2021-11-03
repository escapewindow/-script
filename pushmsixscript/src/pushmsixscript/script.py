#!/usr/bin/env python3
""" Push msix Script main script
"""
import logging
import os

from scriptworker import client

from pushmsixscript import artifacts, microsoft_store, task

log = logging.getLogger(__name__)


async def async_main(context):
    context.task = client.get_task(context.config)

    # TODO Sanity checks on the file
    msix_file_path = artifacts.get_msix_file_path(context)
    channel = task.get_msix_channel(context.config, context.task)

    _log_warning_forewords(context.config, channel)

    microsoft_store.push(context, msix_file_path, channel)


def _log_warning_forewords(config, channel):
    if not task.is_allowed_to_push_to_microsoft_store(config, channel):
        log.warning("Insufficient rights to reach Microsoft Store: *All* requests will be mocked.")


def get_default_config(base_dir=None):
    base_dir = base_dir or os.path.dirname(os.getcwd())
    default_config = {
        "work_dir": os.path.join(base_dir, "work_dir"),
        "schema_file": os.path.join(os.path.dirname(__file__), "data", "push_msix_task_schema.json"),
        "verbose": False,
    }
    return default_config


def main(config_path=None):
    return client.sync_main(async_main, config_path=config_path, default_config=get_default_config())


__name__ == "__main__" and main()
