from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='rankaggregation',
    version='0.1.2',  # TODO: automatically sync this with __init__.py
    description='Python implementations of rank aggregation methods for ranked lists.',
    long_description=readme(),
    keywords='rank aggregation ranked lists instant runoff irv borda count',
    url='https://github.com/djcunningham0/rankaggregation',
    author='Danny Cunningham',
    author_email='djcunningham0@gmail.com',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering'
    ]
)
