#!/usr/bin/env python
"""Shared functions for iScript.

Attributes:
    log (logging.Logger): the log object for the module

"""

import glob
import logging
import os
from copy import deepcopy

from iscript.constants import PRODUCT_CONFIG
from iscript.exceptions import IScriptError

log = logging.getLogger(__name__)

_CERT_TYPE_TO_KEY_CONFIG = {"dep-signing": "dep", "nightly-signing": "nightly", "release-signing": "release"}


def task_cert_type(config, task):
    """Get the signing cert type from the task scopes.

    Args:
        config (dict): the running config
        task (dict): the running task

    Returns:
        str: the cert type, e.g. ``dep-signing``

    """
    cert_prefix = "{}cert:".format(config["taskcluster_scope_prefix"])
    cert_scopes = [i for i in task["scopes"] if i.startswith(cert_prefix)]
    if len(cert_scopes) > 1:
        raise IScriptError("Too many cert scopes found! {}".format(cert_scopes))
    if len(cert_scopes) < 1:
        raise IScriptError("Unable to find a cert scope! {}".format(task["scopes"]))
    return cert_scopes[0].replace(cert_prefix, "")


def get_product(task):
    """Get the product from the task definition.

    Args:
        task (dict): the running task

    Returns:
        str: ``task.payload.product``, if set. Defaults to ``firefox``

    """
    return task["payload"].get("product", "firefox")


def get_sign_config(config, task, base_key="mac_config"):
    """Sanity check the task scopes and return the appropriate ``sign_config``.

    The ``sign_config`` is, e.g. the ``config.mac_config.dep`` dictionary,
    for mac dep-signing, with product config baked in as well.

    Args:
        config (dict): the running config
        task (dict): the running task
        base_key (str, optional): the base key in the dictionary. Defaults to
            ``mac_config``.

    Raises:
        IScriptError: on failure to verify the scopes.

    Returns:
        dict: the ``sign_config``

    """
    try:
        cert_type = task_cert_type(config, task)
        sign_config = deepcopy(PRODUCT_CONFIG[base_key][get_product(task)])
        sign_config.update(config[base_key][_CERT_TYPE_TO_KEY_CONFIG[cert_type]])
        sign_config["release_type"] = _CERT_TYPE_TO_KEY_CONFIG[cert_type]
        return sign_config
    except KeyError as exc:
        raise IScriptError("get_sign_config error: {}".format(str(exc))) from exc


def expand_globs(globs, parent_dir=None):
    """Expand globs in a directory.

    Args:
        globs (list): a list of glob strings.
        parent_dir (str, optional): the parent directory to look in. Will default
            to cwd.

    """
    parent_dir = parent_dir or os.getcwd()
    paths = []
    for path_glob in globs:
        path_glob = os.path.join(parent_dir, path_glob)
        for path in glob.glob(path_glob, recursive=True):
            paths.append(os.path.relpath(path, start=parent_dir))
    return sorted(list(set(paths)))
