from setuptools import find_packages, setup

setup(
    name='vidsage',
    packages=find_packages(include=['src', 'logger_module']),
    version='0.1.0',
    description='A smart video recommendation platform that understands your commands or searches to suggest and provide recommendations based on your preferences, including multiple video searches.',
    author='sameer',
    license='GNU',
)
