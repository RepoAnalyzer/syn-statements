from projen.python import PythonProject

project = PythonProject(
    author_email="46250621+DeadlySquad13@users.noreply.github.com",
    author_name="DeadlySquad13",
    module_name="projen_test3",
    name="projen-test3",
    version="0.1.0",
)

project.synth()