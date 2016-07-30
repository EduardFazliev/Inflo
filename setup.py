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
        install_requires=[
            'requests',
            'simple-crypt',
            'prettytable'
        ]
)
