from setuptools import setup

setup(
    name='aerotropolis_app',
    packages=["aerotropolis_app"],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_wtf',
        'pymongo',
        'boto3'
    ],
)