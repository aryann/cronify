import os
import setuptools


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name='schedulify',
    version='0.0.1',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
    description=('Schedule Python functions on Google Cloud Platform '
                 'with minimal boilerplate'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=[
        'schedulify',
    ],
    package_dir={
        '': 'src',
    },
    package_data={
        'schedulify': [
            'Dockerfile',
            '.dockerignore',
        ],
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'schedulify=schedulify:main',
        ],
    },
)
