from trello import TrelloApi
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--client-api-key", help="your app's client api key",
                    action="store", required=True)
parser.add_argument("-a", "--app-name", help="your app's name",
                    action="store", required=True)
parser.add_argument("-e", "--expiration",
                    help="the token's expiration, defaults to 30days",
                    default='30days', action="store")
parser.add_argument("-w", "--write-access", help="the token has write access",
                    default=False, action="store_true")
args = vars(parser.parse_args())

print("Access the following link to generate your access token:")
trello = TrelloApi(args['client_api_key'])
print(trello.get_token_url(args['app_name'], expires=args['expiration'],
                           write_access=args['write_access']))
