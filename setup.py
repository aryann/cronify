import setuptools

setuptools.setup(
    name='schedulify',
    version='0.0.1',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
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
