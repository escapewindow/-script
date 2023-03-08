# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
Tox-specific transforms
"""


from taskgraph.transforms.base import TransformSequence

transforms = TransformSequence()


@transforms.add
def add_dependencies(config, tasks):
    """Explicitly add the docker-image task as a dependency.

    This needs to be done before the `cached_tasks` transform, so we can't
    wait until the `build_docker_worker_payload` transform.

    From `build_docker_worker_payload`.

    """
    for task in tasks:
        image = task["worker"]["docker-image"]
        if isinstance(image, dict):
            if "in-tree" in image:
                _name = image["in-tree"]
                docker_image_task = "build-docker-image-" + image["in-tree"]
                task.setdefault("dependencies", {})["docker-image"] = docker_image_task
        yield task
