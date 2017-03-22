from setuptools import setup, find_packages

# Setup configuration for the tool
setup(
    name='RTX',
    version='0.2',
    long_description="Real-Time Experimentation (RTX) tool allows for self-adaptation based on analysis of real time (streaming) data. RTX is particularly useful in analyzing operational data in a Big Data environement.",
    packages=find_packages(),
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'colorama',  # color on the console
        'kafka-python',  # integration with kafka
        'scikit-optimize',  # gauss optimizer
        'flask',  # json support
        'pandas',  # plotting lib
        'seaborn',  # plotting lib
        'paho-mqtt',  # mqtt integration
        'requests'  # http integreation
    ]
)
