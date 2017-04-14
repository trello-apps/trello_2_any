from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
import requests


def get_oauth_token(client_api_key, client_api_secret, app_name, expiration='30days', scope='read'):
    '''
    Retrieves an access token from Trello using OAuth1

        client_api_key => the application key created at https://trello.com/app-key

        client_api_secret => the secret key provided also at https://trello.com/app-key

        app_name => the application name as it will appear in https://trello.com/me/account

        expiration => string, expiration period of the access token, defaults to '30days'

        scope => string, scope permissions of your token, default to 'read' (other possible value 'read,write')

    :return: access_token
    '''
    request_token_url = 'https://trello.com/1/OAuthGetRequestToken'
    authorize_url = 'https://trello.com/1/OAuthAuthorizeToken'
    access_token_url = 'https://trello.com/1/OAuthGetAccessToken'

    oauth = OAuth1Session(client_api_key, client_secret=client_api_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    authorization_url = oauth.authorization_url(authorize_url + '?name=%s&expiration=%s&scope=%s' % (app_name, expiration, scope))

    print('Please go here and authorize,', authorization_url)
    oauth_verifier = raw_input('Paste the full verification code here: ')
    session = OAuth1Session(client_api_key,
                            client_secret=client_api_secret,
                            resource_owner_key=resource_owner_key,
                            resource_owner_secret=resource_owner_secret,
                            verifier=oauth_verifier)
    access_token = session.fetch_access_token(access_token_url)
    print("Access token:")
    print(access_token['oauth_token'])
    print("Access token secret")
    print(access_token['oauth_token_secret'])
    return access_token


def get_auth():
    # TODO give possibility to pass trello secret keys via environment variables

    from secrets.api import TRELLO_API_KEY, TRELLO_API_SECRET, TOKEN, TOKEN_SECRET

    oauth = OAuth1(client_key=TRELLO_API_KEY,
                   client_secret=TRELLO_API_SECRET,
                   resource_owner_key=TOKEN,
                   resource_owner_secret=TOKEN_SECRET)
    return oauth


if __name__ == '__main__':
    # FIXME add argparse and allow to request new token
    auth = get_auth()
    r = requests.get('https://api.trello.com/1/member/me/boards', auth=auth)
    if r.status_code == 401:
        raise Exception('Your request is not authorized, please validate your access token in secrets.api')
    if r.status_code != 200:
        raise Exception('Your request has failed, please validate your access token in secrets.api')
