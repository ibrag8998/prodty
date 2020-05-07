from setuptools import setup


setup(
    name='prodty',
    version='1.0.0',
    packages=['prodty'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'dateparser',
    ],
)

