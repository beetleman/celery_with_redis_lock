import setuptools

with open('README.md') as readme_file:
    README = readme_file.read().strip()

setuptools.setup(
    name="celery_with_redis_lock",
    version="0.1.0",
    url="example.com",

    author="Mateusz Pro.",
    author_email="mateusz.probachta@gmail.com",

    description="testing",
    long_description=README,

    packages=setuptools.find_packages(),

    install_requires=[
        'redis',
        'Celery',
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
