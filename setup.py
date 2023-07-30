from setuptools import setup

is_py3 = sys.version_info >= (3,)

# TODO find a better way than this
if is_py3:
    install_requires = [
        'MarkupSafe',
        'beautifulsoup4',
        'jinja2',
        'requests',
    ]
else:
    # assume py2
    install_requires = [
        'MarkupSafe==1.1.1',
        'beautifulsoup4==4.9.3',
        'jinja2==2.11.3',
        'requests==2.22.0',
    ]


setup(
    name='pypub',
    version='1.6',
    packages=['pypub',],
    package_data={'pypub': ['epub_templates/*',]},
    author = 'Chris Clark',
    author_email = 'clach04@gmail.com',
    url = 'https://github.com/clach04/pypub',
    license='MIT',
    install_requires=install_requires,
    description= "Create epub's using python. Pypub is a python library to create epub files quickly without having to worry about the intricacies of the epub specification.",
)
# TODO long description from readme
# TODO py 2.7 and other classifiers
