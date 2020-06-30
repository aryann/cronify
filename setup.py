import setuptools

setuptools.setup(
    name='cronify',
    version='0.0.1',
    packages=setuptools.find_packages(),
    scripts=[
        'bin/cronify',
    ],
    include_package_data=True,
)
