from setuptools import setup, find_packages

setup(
        name='inflo',
        version='0.0.1',
        packages=find_packages(),
        url='https://github.com/EduardFazliev/inflo',
        license='MIT',
        author='Eduard Fazliev',
        author_email='napalmedd@gmail.com',
        description='',
        scripts=['bin/inflo'],
        test_suite='nose.collector',
        install_requires=[
            'requests',
            'simple-crypt',
            'prettytable',
        ],
        tests_requires=[
            'nose',
            'mock'
        ]
)
