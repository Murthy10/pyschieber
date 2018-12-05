import setuptools

setuptools.setup(
    name='schieber',
    version='0.1.5',
    description='Schieber is a terminal application of the popular swiss card game Schieber and provides an API to the game',
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    author='Joel Niklaus',
    author_email='me@joelniklaus.ch',
    url='https://github.com/JoelNiklaus/schieber',
    license=open('LICENSE', "r").read(),
    packages=setuptools.find_packages(exclude=('tests', 'docs')),
    scripts=['bin/schieber'],
)
