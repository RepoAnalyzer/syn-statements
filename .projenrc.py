import os

from projen import SampleDir, SampleFile, YamlFile
from projen.python import PythonProject

MODULE_NAME = "projen_template"

# Folders holding all our modules with code.
ROOT_MODULE_DIR = "src"
ROOT_TEST_DIR = "tests"


class PythonRepoAnalyzerProject(PythonProject):
    black = None
    flake8 = None
    isort = None

    pre_commit = None

    def __init__(self, black=True, flake8=True, isort=True, pre_commit=True, **options):
        super(PythonRepoAnalyzerProject, self).__init__(**options)
        self.gitignore.exclude(".venv_win")

        if black:
            self.black = True
            self.add_dev_dependency("black@^22")

        if flake8:
            self.flake8 = SampleFile(
                self,
                ".flake8",
                contents="\n".join(
                    ["[flake8] max-line-length = 88", "extend-ignore = E203"]
                ),
            )
            self.add_dev_dependency("flake8@^5")

        if isort:
            self.isort = SampleFile(
                self,
                ".isort.cfg",
                contents="\n".join(["[settings]", 'profile = "black"']),
            )
            self.add_dev_dependency("isort@^5")

        if pre_commit:
            contents = {
                "files": f"{ROOT_MODULE_DIR}\/.*|{ROOT_TEST_DIR}\/.*",  # src and test files.
                "repos": [
                    {
                        "repo": "https://github.com/pre-commit/pre-commit-hooks",
                        "rev": "v2.3.0",
                        "hooks": [
                            {"id": "trailing-whitespace"},
                            {"id": "end-of-file-fixer"},
                            {"id": "check-yaml"},
                            {"id": "check-added-large-files"},
                        ],
                    }
                ],
            }

            if self.black:
                contents["repos"].append(
                    {
                        "repo": "https://github.com/psf/black",
                        "rev": "22.10.0",
                        "hooks": [
                            {"id": "black"},
                        ],
                    },
                )

            if self.flake8:
                contents["repos"].append(
                    {
                        "repo": "https://gitlab.com/pycqa/flake8",
                        "rev": "5.0.4",
                        "hooks": [
                            {"id": "flake8"},
                        ],
                    },
                )

            self.pre_commit = YamlFile(
                self,
                ".pre-commit-config.yaml",
                obj=contents,
            )


project = PythonRepoAnalyzerProject(
    author_email="46250621+DeadlySquad13@users.noreply.github.com",
    author_name="DeadlySquad13",
    module_name=MODULE_NAME,
    name="projen_template",
    version="0.1.0",
    pytest_options={"testdir": f"{ROOT_TEST_DIR}/{MODULE_NAME}"},
    setuptools=True,
    black=True,
    flake8=True,
    isort=True,
    dev_deps=[
        "pytest",
    ],
    sample=False,  # Overriden by custom sample dir.
)

# From root.
pythonLibSample = SampleDir(
    project,
    f"{ROOT_MODULE_DIR}/{project.module_name}",
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

project.synth()
