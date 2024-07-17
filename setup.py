from setuptools import setup, find_packages

setup(
    name='error_correction',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ldpc==0.1.50',
        'numpy==1.26.2',
    ],
)