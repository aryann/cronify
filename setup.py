import os
import setuptools


with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                       'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name='schedulify',
    version='0.0.3',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
    description=('Schedule Python functions on Google Cloud Platform '
                 'with minimal boilerplate'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/aryann/schedulify',
    project_urls={
        'Source Code': 'https://github.com/aryann/schedulify',
        "Author's Website": 'https://aryan.app',
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
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
