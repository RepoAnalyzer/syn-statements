from projen.python import PythonProject

project = PythonProject(
    author_email='46250621+DeadlySquad13@users.noreply.github.com',
    author_name='DeadlySquad13',
    module_name='projen_template',
    name='projen_template',
    version='0.1.0',

    setuptools=True,

    dev_deps=[
        'pytest'
        'black'
    ],
)

project.synth()
