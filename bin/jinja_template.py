import argparse

import jinja2
from trello import TrelloApi

from trello_model.converter import TrelloConverter

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client-api-key", help="your app's client api key",
                    action="store", required=True)
parser.add_argument("-t", "--token", help="your app's access token",
                    action="store", required=True)
parser.add_argument("-b", "--board-id", help="your trello board id",
                    action="store", required=True)
args = vars(parser.parse_args())

trello = TrelloApi(args['client_api_key'])
trello.set_token(args['token'])

converter = TrelloConverter(trello, args['board_id'])

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
converter.to_template(jinja2.Template(template,
                                      trim_blocks=True,
                                      lstrip_blocks=True))
