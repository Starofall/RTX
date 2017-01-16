from setuptools import setup, find_packages

setup(
    name='RTX',
    version='0.1',
    long_description="real-time experimentation",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'colorama',
        'kafka-python',
        'scikit-optimize',
        'flask'
    ]
)