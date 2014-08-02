from setuptools import setup, Command
from jbio.testframework import auto_load_tests

def readme():
    with open('README') as f:
        return f.read()

class TestRunner(Command):
    description = "Custom function"
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import jbio.test
        auto_load_tests(jbio.test)()
        
setup(name='jbio',
      version='0.1',
      description='General Tools',
      long_description=readme(),
      url='https://github.com/jgurtowski/jbio',
      author='James Gurtowski',
      author_email='gurtowsk@cshl.edu',
      license='GPL',
      packages=['jbio'],
      cmdclass = {'test': TestRunner},
      )
      
      
      
      
