from setuptools import setup

with open("./NUCT/requirements.txt", "r") as f:
    requires = f.read().split("\n")

setup(
    name="nuct-cli",
    version="0.0.1-beta",
    install_requires=requires,
    extras_require={
        "develop": ["pytest"],
    },
    entry_points={
        "console_scripts": [
            "nuct-cli = NUCT.cli:nuct"
        ],
    }
)