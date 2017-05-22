from setuptools import setup, find_packages

setup(
    name='funcy-task-engine',
    version='0.0.1dev',
    packages=find_packages(),
    include_package_data=True,
    # install_requires=INSTALL_REQUIRES,
    scripts=['bin/funcy-task-engine.py']
)