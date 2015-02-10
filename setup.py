import os
from setuptools import setup, find_packages

def readfile(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='wikipedia-ner',
    version='0.0.19',
    description='Python package for creating labeled examples from wiki dumps',
    long_description=readfile('README.md'),
    ext_modules=[],
    packages=find_packages(),
    author='Jonathan Raiman',
    author_email='jraiman at mit dot edu',
    url='https://github.com/JonathanRaiman/wikipedia_ner',
    download_url='https://github.com/JonathanRaiman/wikipedia_ner',
    keywords='XML, epub, tokenization, NLP',
    license='MIT',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing :: Linguistic',
    ],
    # test_suite="something.test",
    setup_requires = [],
    install_requires=[
        'xml_cleaner',
        'epub_conversion'
    ],
    include_package_data=True,
)