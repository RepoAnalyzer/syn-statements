import os

from projen import SampleDir, SampleFile
from projen.python import PythonProject

MODULE_NAME = "projen_template"

project = PythonProject(
    author_email="46250621+DeadlySquad13@users.noreply.github.com",
    author_name="DeadlySquad13",
    module_name=MODULE_NAME,
    name="projen_template",
    version="0.1.0",
    pytest_options={"testdir": f"tests/{MODULE_NAME}"},
    setuptools=True,
    dev_deps=[
        "pytest",
        "black",
        "flake8",
    ],
    sample=False,  # Overriden by custom sample dir.
)

# Test exmaple.
pythonLibSample = SampleDir(
    project,
    f"src/{project.module_name}",
    files={
        "__init__.py": '__version__ = "0.1.0"\n',
        "__main__.py": "\n".join(
            [
                "from .example import hello",
                "",
                'if __name__ == "__main__":',
                '    name = input("What is your name? ")',
                "    print(hello(name))",
                "",
            ]
        ),
        "example.py": "\n".join(
            [
                "def hello(name: str) -> str:",
                '    """A simple greeting.',
                "    Args:",
                "        name (str): Name to greet.",
                "    Returns:",
                "        str: greeting message",
                '    """',
                '    return f"Hello {name}!"',
                "",
            ]
        ),
    },
)

flake8 = SampleFile(
    project,
    ".flake8",
    contents="\n".join(["[flake8] max-line-length = 88", "extend-ignore = E203"]),
)

isort = SampleFile(
    project,
    ".isort.cfg",
    contents="\n".join(["[settings]", 'profile = "black"']),
)


project.synth()
