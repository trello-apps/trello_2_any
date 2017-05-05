# Trello 2 Any

## Getting started

Install via setup.py

```
cd trello_2_any/
python setup.py install # or pip install .
```

Or, clone the repository from git and add its path to `PYTHONPATH`

```
$ git clone https://github.com/trello-apps/trello_2_any.git

$ export PYTHONPATH=trello_2_any/:$PYTHONPATH

$ python trello_2_any/bin/sample.py -h
usage: sample.py [-h] -c CLIENT_API_KEY -t TOKEN -b BOARD_ID

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_API_KEY, --client-api-key CLIENT_API_KEY
                        your app's client api key
  -t TOKEN, --token TOKEN
                        your app's access token
  -b BOARD_ID, --board-id BOARD_ID
                        your trello board id
```

## Access Tokens

In order to be able to access your Trello's boards, first you need to generate an access token.

1. Go to https://trello.com/app-key, and retrieve your application key.
2. Run `./bin/generate_access_token.py` as described below and open the link it prints.

```
$ python bin/generate_access_token.py -h
usage: generate_access_token.py [-h] -c CLIENT_API_KEY -a APP_NAME
                                [-e EXPIRATION] [-w]

optional arguments:
  -h, --help            show this help message and exit
  -c CLIENT_API_KEY, --client-api-key CLIENT_API_KEY
                        your app's client api key
  -a APP_NAME, --app-name APP_NAME
                        your app's name
  -e EXPIRATION, --expiration EXPIRATION
                        the token's expiration, defaults to 30days
  -w, --write-access    the token has write access


$ python ./bin/generate_access_token.py --client-api-key <my_app_key> --app-name TEST
Access the following link to generate your access token:
https://trello.com/1/authorize?key=my_app_key&name=TEST&expiration=30days&response_type=token&scope=read
```

3. Copy the generated token to a place safe!

## Available Transformers

- Markdown
- AsciiDoc
- Atlassian Confluence 

### Sample

The following will retrieve all Trello lists from a given Trello board, and print it to stdout using a specific transformer:

```
trello = TrelloApi(args['client_api_key'])
trello.set_token(args['token'])
extraction = TrelloExtraction(trello, args['board_id'])
print(extraction.apply_transformer(MarkdownTransformer()))
```

## Jinja2 Templating

You can also apply a Jinja2 template to render the board items.

The rendering is called with the following context:
- {'title', board_name, 'board_lists': board_lists}
    - `board_lists` is a list of `List = namedtuple('List', ['id', 'name', 'cards'])`
    - `cards` is a list of `Card = namedtuple('Card', ['id', 'name', 'comments', 'voters'])`
    - `comments` is a list of `Comment = namedtuple('Comment', ['text', 'author'])`
    - `voters` is a list of strings containing the full name of each  voter

An example is given in `bin/jinja_template.py`.

```
extraction = TrelloExtraction(trello, args['board_id'])

template = '''
# {{ title }}

{% for board_list in board_lists %}
## {{ board_list.name }}
    {% for card in board_list.cards %}
- {{ card.name }}
        {% if card.comments %}
            {% for comment in card.comments %}
    - comment by {{ comment.author }}: {{ comment.text }}
            {% endfor %}
        {% endif %}
        {% if card.voters %}
    - {{ card.voters|length }} vote(s), by: {{ card.voters | join(', ') }}
        {% endif %}
    {% endfor %}

{% endfor %}
'''
extraction.apply_template(jinja2.Template(template,
                                          trim_blocks=True,
                                          lstrip_blocks=True))
```

## Compatibility

It is compatible with both python 2.7+ and python 3.4+.
Py3 requires the installation of [trello3](https://github.com/waynew/trello3) which is not available on pypi.
