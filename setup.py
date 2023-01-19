from setuptools import setup, find_packages

import illumina_run_monitor

setup(
    name='illumina-run-monitor',
    version=illumina_run_monitor.__version__,
    description='',
    author='Dan Fornika',
    author_email='dan.fornika@bccdc.ca',
    url='https://github.com/BCCDC-PHL/illumina-run-monitor',
    packages=find_packages(exclude=('tests', 'tests.*')),
    python_requires='>=3.10',
    install_requires=[
        "watchdog==2.1.9",
        "requests==2.28.2",
    ],
    setup_requires=['pytest-runner', 'flake8'],
    tests_require=[],
    entry_points = {
        'console_scripts': [
            "monitor-dir = illumina_run_monitor.main:main",
        ],
    }
)
