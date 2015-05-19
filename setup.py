from setuptools import setup

setup(
    name='foreman-ssh',
    version='0.1',
    py_modules=['foreman_ssh'],
    install_requires=[
        'click',
        'requests',
        'parallel-ssh'
    ],
    entry_points='''
        [console_scripts]
        foreman-ssh=foreman_ssh.foreman_ssh:main
    ''',
)
