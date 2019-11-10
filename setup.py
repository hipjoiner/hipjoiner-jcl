from setuptools import setup, find_namespace_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='hipjoiner-jcl',
    version='2019.10.28',
    author='John Pirie',
    author_email='john@thepiries.net',
    description='Task runner & manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hipjoiner/hipjoiner-jcl',
    packages=find_namespace_packages(include=['hipjoiner.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'jcl = hipjoiner.jcl.cli:entry_point',
        ],
    }
)
