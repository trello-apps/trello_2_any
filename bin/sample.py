import argparse

from trello import TrelloApi

from trello_model.converter import TrelloConverter, Target

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

print(converter.to(Target.MARKDOWN))
print("-" * 100)
print(converter.to(Target.ASCIIDOC))
print("-" * 100)
print(converter.to(Target.CONFLUENCE))
