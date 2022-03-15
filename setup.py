from setuptools import find_packages, setup

setup(
    name='netbox-access-lists',
    version='0.1',
    description='An example NetBox plugin',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)

