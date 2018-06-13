from setuptools import setup

setup(
    name='faas',
    packages=['faas'],
    include_package_data=True,
    install_requires=[
        'flask',
        'pyyaml',
        'psutil',
        'requests'
    ],
)
