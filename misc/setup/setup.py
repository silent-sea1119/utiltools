from setuptools import setup, find_packages

VER='0.0.1'

with open('version.txt', 'w') as f:
   f.write(VER)

setup(
   name='utiltools',
   version=VER,
   author='Konstantin Kowalski',
   author_email='kostelkow@gmail.com',
   packages=['utiltools'], #, 'utiltools.shellutils'],
   package_dir={'utiltools': '../../src'},
   description='Misc tools'
)
