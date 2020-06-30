import setuptools

setuptools.setup(
    name='cronify',
    version='0.0.1',
    author='Aryan Naraghi',
    author_email='aryan.naraghi@gmail.com',
    packages=[
        'cronify',
    ],
    package_dir={
        '': 'src',
    },
    package_data={
        'cronify': [
            'Dockerfile',
            '.dockerignore',
        ],
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'cronify=cronify:main',
        ],
    },
)
