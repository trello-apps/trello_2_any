from trello import TrelloApi

from trello_model import TrelloExtraction
from trello_transformers import MarkdownTransformer, AsciiDocTransformer, \
                                ConfluenceTransformer

import argparse

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

extraction = TrelloExtraction(trello, args['board_id'])
extraction.apply_transformer(MarkdownTransformer())
print("-" * 100)
extraction.apply_transformer(AsciiDocTransformer())
print("-" * 100)
extraction.apply_transformer(ConfluenceTransformer())
