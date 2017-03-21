from setuptools import setup, find_packages

setup(
    name='spellbound',
    description='',
    author='Mathieu Sabourin',
    author_email='mathieu.c.sabourin@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'spellbound = spellbound.cli.main:main'
        ]
    }
)
