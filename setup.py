import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='jcl',
    version='2019.5.20',
    author='John Pirie',
    author_email='john@thepiries.net',
    description='Task runner & manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jwpirie/jcl',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'jcl = jcl.main:entry',
        ],
    }
)
