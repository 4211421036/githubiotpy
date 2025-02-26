from setuptools import setup

setup(
    name='githubiot',
    version='1.0.0',
    py_modules=['githubiot_cli'],
    install_requires=[
        'requests',
        'matplotlib',
        'pyinstaller'
    ],
    entry_points={
        'console_scripts': [
            'githubiot=githubiot_cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
)