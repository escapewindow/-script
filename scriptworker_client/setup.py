import os
from glob import glob

from setuptools import find_packages, setup

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "version.txt")) as f:
    version = f.read().rstrip()

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "requirements", "base.in")
) as f:
    install_requires = f.read().splitlines()

setup(
    name="scriptworker_client",
    version=version,
    description="Scriptworker *script shared code",
    author="Mozilla Release Engineering",
    author_email="release+python@mozilla.com",
    url="https://github.com/escapewindow/scriptworker-scripts/tree/master/scriptworker-client",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(path))[0] for path in glob("src/*.py")
    ],
    include_package_data=True,
    zip_safe=True,
    license="MPL2",
    install_requires=install_requires,
)
