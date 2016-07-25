import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='emailoto',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Django authentication using one-time-only email tokens',
    long_description=README,
    url='https://github.com/qdonnellan/django_emailoto',
    author='Quentin Donnellan',
    author_email='quentin@qdonnellan.com',
    test_suite="runtests",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
