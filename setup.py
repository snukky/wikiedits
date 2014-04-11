from distutils.core import setup

setup(
    name='WikiEdits',
    version='0.1.0',
    author='snukky',
    author_email='snk987@gmail.com',
    packages=['wiki_edits'],
    scripts=['bin/extract_edits.py', 'bin/extract_wiki_edits.py'],
    license='LICENSE.txt',
    description='Automatic extraction of edited sentences from text edition histories.',
    long_description=open('README.txt').read(),
)
