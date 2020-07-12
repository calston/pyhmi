from setuptools import setup, find_packages

setup(
    name='pyhmi',
    version='0.0.1',
    url='http://github.com/calston/pyhmi',
    description='A library for building human-machine interfaces',
    classifiers=[
        "Programming Language :: Python",
    ],
    author='Colin Alston',
    author_email='colin.alston@gmail.com',
    license='BSD',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'PyYAML'
    ],
)
