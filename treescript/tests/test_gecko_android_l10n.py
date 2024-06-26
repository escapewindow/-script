import os
import shutil

import pytest

import treescript.gecko.android_l10n as android_l10n
import treescript.gecko.mercurial as mercurial

from unittest.mock import AsyncMock


async def noop_async(*args, **kwargs):
    pass


# build_commit_message {{{1
@pytest.mark.parametrize("dontbuild, ignore_closed_tree", ((True, True), (False, False)))
def test_build_commit_message(dontbuild, ignore_closed_tree):
    """build_commit_message adds the correct approval strings"""
    expected = "no bug - DESCRIPTION r=release a=l10n"
    if dontbuild:
        expected += android_l10n.DONTBUILD_MSG
    if ignore_closed_tree:
        expected += android_l10n.CLOSED_TREE_MSG
    assert android_l10n.build_commit_message("DESCRIPTION", dontbuild=dontbuild, ignore_closed_tree=ignore_closed_tree).rstrip() == expected


# get_android_l10n_files_toml {{{1
def test_get_android_l10n_files_toml(mocker):
    toml_contents = """
basepath = "."

locales = [
  "ab",
  "en-GB",
]

[env]

[[paths]]
  reference = "app/src/main/res/values/strings.xml"
  l10n = "app/src/main/res/values-{android_locale}/strings.xml"
"""
    open_mock = mocker.mock_open(read_data=toml_contents)
    mocker.patch("builtins.open", open_mock, create=True)
    mocker.patch.object(os.path, "exists", return_value=True)

    assert android_l10n.get_android_l10n_files_toml("path") == []
    assert android_l10n.get_android_l10n_files_toml("path", "search_path") == []
    mocker.patch.object(android_l10n.paths, "ProjectFiles", return_value=[("l10n-path", "ref-path", "unused", "unused")])
    assert android_l10n.get_android_l10n_files_toml("path") == [
        {"abs_path": "l10n-path", "rel_path": "l10n-path"},
        {"abs_path": "l10n-path", "rel_path": "l10n-path"},
    ]
    assert android_l10n.get_android_l10n_files_toml("path", "search_path") == [
        {"abs_path": "l10n-path", "rel_path": "../l10n-path"},
        {"abs_path": "l10n-path", "rel_path": "../l10n-path"},
    ]


# copy_android_l10n_files {{{1
@pytest.mark.asyncio
async def test_copy_android_l10n_files(mocker):
    mocker.patch.object(os, "makedirs")

    async def check_params(*args, **kwargs):
        assert "add" in args
        assert "dest/relsource" in args

    mocker.patch.object(mercurial, "run_hg_command", new=check_params)

    copy = mocker.patch.object(shutil, "copy2")
    await android_l10n.copy_android_l10n_files({}, [{"abs_path": "abssource", "rel_path": "relsource"}], None, "dest")
    copy.assert_called_with("abssource", "dest/relsource")
    await android_l10n.copy_android_l10n_files({}, [{"abs_path": "abssource", "rel_path": "relsource"}], "src", "dest")
    copy.assert_called_with("src/relsource", "dest/relsource")


# android_l10n_action {{{1
@pytest.mark.asyncio
async def test_android_l10n_action(mocker):

    async def check_treestatus(*args):
        return True

    mocker.patch.object(os, "makedirs")
    mocker.patch.object(shutil, "copy2")
    mocker.patch.object(android_l10n, "get_dontbuild", return_value=False)
    mocker.patch.object(android_l10n, "get_ignore_closed_tree", return_value=True)
    mocker.patch.object(android_l10n, "check_treestatus", new=check_treestatus)
    mocker.patch.object(android_l10n, "vcs", new=AsyncMock())
    mocker.patch.object(android_l10n, "get_android_l10n_files_toml", return_value=["l10n1", "l10n2"])
    copy = mocker.patch.object(android_l10n, "copy_android_l10n_files")

    task_info = {"from_repo_url": "x", "toml_info": [{"toml_path": "x/y.toml", "dest_path": "x"}]}

    # like import
    await android_l10n.android_l10n_action({}, {}, task_info, "repo/path", "fromrepo/path", "", "", None, "dest_path")
    copy.assert_called_with({}, ["l10n1", "l10n2"], None, "repo/path/x")
    # like sync
    await android_l10n.android_l10n_action({}, {}, task_info, "repo/path", "fromrepo/path", "", "", "srcpath", None)
    copy.assert_called_with({}, ["l10n1", "l10n2"], "srcpath", "repo/path")


# android_l10n_import {{{1
@pytest.mark.parametrize(
    "ignore_closed_tree, android_l10n_import_info, old_contents, new_contents, changes",
    (
        (
            True,
            {"from_repo_url": "x", "toml_info": [{"toml_path": "x/y.toml", "dest_path": "x"}]},
            {"one": {"revision": "onerev", "platforms": ["platform"]}, "two": {"revision": "tworev", "platforms": ["platform"]}},
            {"one": {"revision": "onerev", "platforms": ["platform"]}, "two": {"revision": "tworev", "platforms": ["platform"]}},
            1,
        ),
        (
            False,
            {"from_repo_url": "x", "toml_info": [{"toml_path": "x/y.toml", "dest_path": "x"}]},
            {"one": {"revision": "oldonerev", "platforms": ["platform"]}, "two": {"revision": "oldtworev", "platforms": ["platform"]}},
            {"one": {"revision": "newonerev", "platforms": ["platform"]}, "two": {"revision": "newtworev", "platforms": ["platform"]}},
            1,
        ),
    ),
)
@pytest.mark.asyncio
async def test_android_l10n_import(mocker, ignore_closed_tree, android_l10n_import_info, tmpdir, old_contents, new_contents, changes):
    """android_l10n_import flow coverage."""

    async def check_treestatus(*args):
        return True

    async def fake_build_revision_dict(*args, **kwargs):
        return new_contents

    mocker.patch.object(os, "makedirs")
    mocker.patch.object(shutil, "copy2")
    mocker.patch.object(android_l10n, "get_dontbuild", return_value=False)
    mocker.patch.object(android_l10n, "get_ignore_closed_tree", return_value=ignore_closed_tree)
    mocker.patch.object(android_l10n, "check_treestatus", new=check_treestatus)
    mocker.patch.object(android_l10n, "get_android_l10n_import_info", return_value=android_l10n_import_info)
    mocker.patch.object(android_l10n, "run_command")
    mocker.patch.object(android_l10n, "get_android_l10n_files_toml")
    mocker.patch.object(android_l10n, "copy_android_l10n_files")
    mocker.patch.object(android_l10n, "vcs", new=AsyncMock())

    assert await android_l10n.android_l10n_import({}, {}, tmpdir) == changes


@pytest.mark.asyncio
async def test_android_l10n_import_closed_tree(mocker):
    """android_l10n_import should exit if the tree is closed and ignore_closed_tree is
    False.

    """

    async def check_treestatus(*args):
        return False

    mocker.patch.object(android_l10n, "get_dontbuild", return_value=False)
    mocker.patch.object(android_l10n, "get_ignore_closed_tree", return_value=False)
    mocker.patch.object(android_l10n, "get_short_source_repo", return_value="mozilla-central")
    mocker.patch.object(android_l10n, "check_treestatus", new=check_treestatus)
    mocker.patch.object(android_l10n, "run_command")
    # this will [intentionally] break if we fail to exit android_l10n_import where
    # we're supposed to
    mocker.patch.object(android_l10n, "get_android_l10n_import_info", return_value={"from_repo_url": "x"})

    assert await android_l10n.android_l10n_import({}, {}, "") == 0


# android_l10n_sync {{{1
@pytest.mark.parametrize(
    "ignore_closed_tree, android_l10n_sync_info, old_contents, new_contents, changes",
    (
        (
            True,
            {"from_repo_url": "x", "toml_info": [{"toml_path": "x/y.toml"}]},
            {"one": {"revision": "onerev", "platforms": ["platform"]}, "two": {"revision": "tworev", "platforms": ["platform"]}},
            {"one": {"revision": "onerev", "platforms": ["platform"]}, "two": {"revision": "tworev", "platforms": ["platform"]}},
            1,
        ),
        (
            False,
            {"from_repo_url": "x", "toml_info": [{"toml_path": "x/y.toml"}]},
            {"one": {"revision": "oldonerev", "platforms": ["platform"]}, "two": {"revision": "oldtworev", "platforms": ["platform"]}},
            {"one": {"revision": "newonerev", "platforms": ["platform"]}, "two": {"revision": "newtworev", "platforms": ["platform"]}},
            1,
        ),
    ),
)
@pytest.mark.asyncio
async def test_android_l10n_sync(mocker, ignore_closed_tree, android_l10n_sync_info, tmpdir, old_contents, new_contents, changes):
    """android_l10n_sync flow coverage."""

    async def check_treestatus(*args):
        return True

    async def fake_build_revision_dict(*args, **kwargs):
        return new_contents

    mocker.patch.object(os, "makedirs")
    mocker.patch.object(shutil, "copy2")
    mocker.patch.object(android_l10n, "get_dontbuild", return_value=False)
    mocker.patch.object(android_l10n, "get_ignore_closed_tree", return_value=ignore_closed_tree)
    mocker.patch.object(android_l10n, "check_treestatus", new=check_treestatus)
    mocker.patch.object(android_l10n, "get_android_l10n_sync_info", return_value=android_l10n_sync_info)
    mocker.patch.object(android_l10n, "get_android_l10n_files_toml")
    mocker.patch.object(android_l10n, "copy_android_l10n_files")
    mocker.patch.object(android_l10n, "vcs", new=AsyncMock())

    assert await android_l10n.android_l10n_sync({}, {}, tmpdir) == changes


@pytest.mark.asyncio
async def test_android_l10n_sync_closed_tree(mocker):
    """android_l10n_sync should exit if the tree is closed and ignore_closed_tree is
    False.

    """

    async def check_treestatus(*args):
        return False

    mocker.patch.object(android_l10n, "get_dontbuild", return_value=False)
    mocker.patch.object(android_l10n, "get_ignore_closed_tree", return_value=False)
    mocker.patch.object(android_l10n, "get_short_source_repo", return_value="mozilla-central")
    mocker.patch.object(android_l10n, "check_treestatus", new=check_treestatus)
    mocker.patch.object(android_l10n, "vcs", new=AsyncMock())
    # this will [intentionally] break if we fail to exit android_l10n_sync where
    # we're supposed to
    mocker.patch.object(android_l10n, "get_android_l10n_sync_info", return_value={"from_repo_url": "x"})

    assert await android_l10n.android_l10n_sync({}, {}, "") == 0
