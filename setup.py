from distutils.core import setup

setup(
    name='WikiEdits',
    version='0.2.0',
    author='snukky',
    author_email='snk987@gmail.com',
    packages=['wikiedits'],
    scripts=['bin/txt_edits.py', 'bin/wiki_edits.py'],
    license='LICENSE.txt',
    description='Automatic extraction of edited sentences from text edition histories.',
    long_description=open('README.txt').read(),
)
