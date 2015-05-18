from setuptools import setup

setup(
    name='foreman-ssh',
    version='0.1',
    py_modules=['foremanssh'],
    install_requires=[
        'click',
        'requests',
        'parallel-ssh'
    ],
    entry_points='''
        [console_scripts]
        foreman-ssh=foremanssh:main
    ''',
)
