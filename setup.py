from setuptools import setup

setup(name='trello_2_any',
      version='0.1',
      description='Convert trello boards to any other format (markdown, asciidoc, confluence, ...)',
      url='https://github.com/aayoubi/trello-2-any',
      author='aayoubi, celmasri',
      author_email='',
      license='MIT',
      packages=['trello_transformers', 'trello_model'],
      zip_safe=False)
