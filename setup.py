try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='Rosetta',
      version='0.4.2',
      description='Prototype video player thing',
      author='Matt N',
      author_email='matt.northsky@gmail.com',
      url='https://github.com/mattsky/rosetta',
      entry_points={
          'console_scripts': [
              'rosetta = rosetta:main',
          ],
      },
      python_requires='>=3.4.*',
      install_requires=[
          'nose', 'mock', 'requests', 'python-vlc', 'PySide2'
      ],
     )
