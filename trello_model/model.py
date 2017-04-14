import requests

TRELLO_ACTIONS_URL = 'https://api.trello.com/1/cards/{}/actions'
TRELLO_MEMBERS_URL = 'https://api.trello.com/1/members/{}'
TRELLO_BOARD_URL = 'https://api.trello.com/1/boards/{}'
TRELLO_LISTS_URL = 'https://api.trello.com/1/boards/{}/lists'
TRELLO_CARDS_URL = 'https://api.trello.com/1/lists/{}/cards'


class TrelloCard:
    def __init__(self, blob, auth):
        self.name = blob['name']
        self.id = blob['id']
        self.number_of_comments = int(blob['badges']['comments'])
        self.number_of_votes = int(blob['badges']['votes'])
        self.voters = self._voters_id_to_username(blob['idMembersVoted'], auth) if self.number_of_votes > 0 else []
        self.comments = self._retrieve_comments(auth) if self.number_of_comments > 0 else []

    def _retrieve_comments(self, auth):
        actions = requests.get(TRELLO_ACTIONS_URL.format(self.id), auth=auth).json()
        return [(action['memberCreator']['username'], action['data']['text'])
                for action in actions
                if action['type'] == 'commentCard']

    def _voters_id_to_username(self, voters, auth):
        return map(lambda voter: requests.get(TRELLO_MEMBERS_URL.format(voter), auth=auth).json()['fullName'], voters)


class TrelloList:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards


class TrelloBoard:
    def __init__(self, id, auth):
        self.id = id
        self.auth = auth
        self.name = self.get_board_name()
        self.lists = [TrelloList(l['name'], [TrelloCard(c, auth) for c in self.get_cards(l['id'])]) for l in
                      self.get_lists()]

    def get_lists(self):
        return requests.get(TRELLO_LISTS_URL.format(self.id), auth=self.auth).json()

    def get_cards(self, list_id):
        return requests.get(TRELLO_CARDS_URL.format(list_id), auth=self.auth).json()

    def get_board_name(self):
        return requests.get(TRELLO_BOARD_URL.format(self.id), auth=self.auth).json()['name']

    def apply_transformer(self, transformer):
        print transformer.transform_board_name(self.name)
        for list in self.lists:
            print transformer.transform_list_name(list.name)
            for card in list.cards:
                print transformer.transform_card_name(card.name)
                if card.number_of_comments > 0:
                    for author, comment in card.comments:
                        print transformer.transform_card_comment(comment, author)
                if card.number_of_votes > 0:
                    print transformer.transform_card_votes(card.voters)
