from setuptools import setup, find_packages

VER='0.0.1'

with open('version.txt', 'w') as f:
   f.write(VER)

setup(
   name='utiltools',
   version=VER,
   author='Konstantin Kowalski',
   author_email='kostelkow@gmail.com',
   packages=['utiltools', 'utiltools.dbutils'], #, 'utiltools.bfsrs'], #, 'utiltools.shellutils'],
   package_dir={'utiltools': '../../src', 'dbutils': '../../src/dbutils'] #, 'bfsrs':'../../src/bfsrs'},
   description='Misc tools',
   install_requires=[
      'gunicorn', 'user_agents', 'sh',
      'Flask', 'Flask-Limiter', 'Flask-Session'
   ]
)
