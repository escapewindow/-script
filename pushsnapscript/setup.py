import os

from setuptools import find_packages, setup

project_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(project_dir, "version.txt")) as f:
    version = f.read().rstrip()

# We allow commented lines in this file
with open(os.path.join(project_dir, "requirements/base.in")) as f:
    requirements = [line.rstrip("\n") for line in f if not line.startswith("#")]


setup(
    name="pushsnapscript",
    version=version,
    description="TaskCluster Ship-It Worker",
    author="Mozilla Release Engineering",
    author_email="release+python@mozilla.com",
    url="https://github.com/mozilla-releng/pushsnapscript",
    packages=find_packages("src"),
    package_data={"pushsnapscript": ["data/*"]},
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["pushsnapscript = pushsnapscript.script:main"]},
    license="MPL2",
    install_requires=requirements,
    classifiers=["Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7"],
)
