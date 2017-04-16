from trello import TrelloApi
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--client-api-key", help="your app's client api key", action="store", required=True)
parser.add_argument("--app-name", help="your app's name", action="store", required=True)
parser.add_argument("--expiration", help="the token's expieration, defaults to 30days", default='30days', action="store")
parser.add_argument("--write-access", help="the token has write access", default=False,action="store_true")
args = vars(parser.parse_args())

print("Access the following link to generate your access token:")
trello = TrelloApi(args['client_api_key'])
print(trello.get_token_url(args['app_name'], expires=args['expiration'], write_access=args['write_access']))

