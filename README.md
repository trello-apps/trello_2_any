# Trello 2 Any

## Getting started

Clone from git and add path to `PYTHONPATH`

```
$ git clone https://github.com/aayoubi/trello_2_any.git
$ export PYTHONPATH=trello_2_any/:$PYTHONPATH
$ python trello_2_any/bin/sample.py -h
usage: sample.py [-h] -c CLIENT_API_KEY -t TOKEN -b BOARD_ID

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_API_KEY, --client-api-key CLIENT_API_KEY
                        your app's client api key
  -t TOKEN, --token TOKEN
                        access token
  -b BOARD_ID, --board-id BOARD_ID
                        your trello board id
```

Or install via setup.py

```
cd trello_2_any/
python setup.py install
# or pip install .
```

## Available Transformers

- Markdown
- AsciiDoc
- Atlassian Confluence 

## Sample

The following will retrieve all Trello lists from a given Trello board, and print it to stdout using a specific transformer:

```
trello = TrelloApi(args['client_api_key'])
trello.set_token(args['token'])
extraction = TrelloExtraction(trello, args['board_id'])
extraction.apply_transformer(MarkdownTransformer())
```

## Compatibility

It is compatible with both python 2.7+ and python 3.4+.
Py3 requires the installation of [trello3](https://github.com/waynew/trello3) which is not available on pypi.
