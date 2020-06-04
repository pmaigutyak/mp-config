
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requires = f.read().splitlines()


version = '4.5'
url = 'https://github.com/pmaigutyak/mp-config'


setup(
    name='django-mp-config',
    version=version,
    description='Django site settings app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, version),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
