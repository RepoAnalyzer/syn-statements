import os
from projen.python import PythonProject
from projen import SampleDir

MODULE_NAME = 'projen_template'

project = PythonProject(
    author_email='46250621+DeadlySquad13@users.noreply.github.com',
    author_name='DeadlySquad13',
    module_name=MODULE_NAME,
    name='projen_template',
    version='0.1.0',

    pytest_options={
        'testdir': f'tests/{MODULE_NAME}'
    },
    setuptools=True,

    dev_deps=[
        'pytest',
        'black',
    ],

    sample=False, # Overriden by custom sample dir.
)

pythonLibSample = SampleDir(project, f'src/{project.module_name}',
    files={
        "__init__.py": '__version__ = "0.1.0"\n',
        "__main__.py": "\n".join([
          "from .example import hello",
          "",
          'if __name__ == "__main__":',
          '    name = input("What is your name? ")',
          "    print(hello(name))",
          "",
        ]),
        "example.py": "\n".join([
          "def hello(name: str) -> str:",
          '    """A simple greeting.',
          "    Args:",
          "        name (str): Name to greet.",
          "    Returns:",
          "        str: greeting message",
          '    """',
          '    return f"Hello {name}!"',
          "",
        ]),
      }
)

project.synth()
