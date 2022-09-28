from setuptools import setup
from setuptools import find_packages

# list dependencies from file
# with open('requirements.txt') as f:
#     content = f.readlines()
# requirements = [x.strip() for x in content]


setup(name='tools_edmz',
      description="tools for icm data exploration",
      packages=find_packages(),
      # install_requires=requirements
      )