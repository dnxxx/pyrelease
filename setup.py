from distutils.core import setup

setup(
    name='release',
    version='1.0.0',
    description='Release',
    py_modules=['release'],

    author='dnxxx',
    author_email='dnx@fbi-security.net',
    license='BSD',

    install_requires=[
        'lazy',
    ]
)
