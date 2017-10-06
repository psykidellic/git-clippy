from setuptools import setup,find_packages

setup(name='git-clippy',
      version='0.1',
      description='You friendly neighborhood code watch',
      url='http://github.com/psykidellic/git-clippy',
      author='Three Blind Cocker Spaniels',
      author_email='psykidellic@example.com',
      license='MIT',
      zip_safe=False,
      packages=find_packages('.'),
      scripts=['bin/git-clippy'],
      install_requires=[
            'clize',
            'gitpython',
            'tqdm'
      ])
