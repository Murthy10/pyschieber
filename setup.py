from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

    setup(
        name='pyschieber',
        version='0.9.4',
        description='pyschieber is a terminal application of the popular swiss card game Schieber and provides an API to the game',
        long_description=readme,
        author='Samuel Kurath',
        author_email='samuel.kurath@gmail.com',
        url='https://github.com/Murthy10/pyschieber',
        license='MIT',
        packages=find_packages(exclude=('tests', 'docs')),
        scripts=['bin/pyschieber'],
    )
