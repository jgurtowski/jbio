from setuptools import setup

def readme():
    with open('README') as f:
        return f.read()

setup(name='jbio',
      version='0.1',
      description='General Tools',
      long_description=readme(),
      url='https://github.com/jgurtowski/jbio',
      author='James Gurtowski',
      author_email='gurtowsk@cshl.edu',
      license='GPL',
      packages=['jbio']
      )
      
      
      
      
