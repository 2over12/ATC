from setuptools import setup

setup(name='anothertextclassifier',
      version='0.1',
      description='If you use this you are probably doing something wrong',
      url='http://github.com/2over12/ATC/',
      author='2over12',
      author_email='ex@ex.com',
      license='MIT',
      packages=['anothertextclassifier'],
      install_requires=['numpy', 'scipy', 'matplotlib', 'ipython', 'jupyter', 'pandas', 'sympy', 'nose'],
      zip_safe=False)
