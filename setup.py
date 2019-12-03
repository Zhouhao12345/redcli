from setuptools import setup, find_packages

setup(
    name="redcli",
    version="1.2.0",
    author="zhouhao",
    python_requires='>=3.7.2',
    author_email="zhouhao19931002@hotmail.com",
    maintainer="zhouhao",
    description="Simple Redis Client Tool",
    packages=find_packages(),
    install_requires=[
        "Pygments == 2.5.1",
        "prompt-toolkit == 3.0.1",
        "click == 7.0",
        "redis == 3.3.1",
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'redcli = redcli.main:redcli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ]
)