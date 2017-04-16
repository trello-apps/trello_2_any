from collections import namedtuple
from collections import defaultdict

Card = namedtuple('Card', ['id', 'name', 'comments', 'voters'])
List = namedtuple('List', ['id', 'name'])


class TrelloExtraction:
    def __init__(self, trello, id):
        self.id = id
        self.trello = trello
        self.name = trello.boards.get(self.id)['name']
        self.board = defaultdict(list)
        for trello_list in trello.boards.get_list(self.id):
            current_list = List(trello_list['id'], trello_list['name'])
            for card in trello.lists.get_card(trello_list['id']):
                comments = [] if card['badges']['comments'] == 0 \
                    else self._retrieve_comments(trello, card['id'])
                voters = [] if card['badges']['votes'] == 0 \
                    else self._voters_id_to_username(trello, card['idMembersVoted'])
                self.board[current_list].append(Card(card['id'], card['name'], comments, voters))

    def _retrieve_comments(self, trello, card_id):
        return [(action['data']['text'], action['memberCreator']['fullName'])
                for action in trello.cards.get_action(card_id)
                if action['type'] == 'commentCard']

    def _voters_id_to_username(self, trello, voters):
        return map(lambda voter: trello.members.get(voter)['fullName'], voters)

    def apply_transformer(self, transformer):
        print transformer.transform_board_name(self.name)
        for list in self.board:
            print transformer.transform_list_name(list.name)
            for card in self.board[list]:
                print transformer.transform_card_name(card.name)
                if len(card.comments) > 0:
                    for comment, author in card.comments:
                        print transformer.transform_card_comment(comment, author)
                if len(card.voters) > 0:
                    print transformer.transform_card_votes(card.voters)
