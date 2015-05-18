from setuptools import setup

setup(
    name='foreman-api',
    version='0.1',
    py_modules=['foremanapi'],
    install_requires=[
        'click',
        'requests',
        'parallel-ssh'
    ],
    entry_points='''
        [console_scripts]
        foreman-api=foremanapi:cli
    ''',
)
