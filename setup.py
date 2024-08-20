from setuptools import setup, find_packages

setup(
    name='error_correction',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.2',
        'networkx==3.2.1',
    ],
)