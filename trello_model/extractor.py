from collections import namedtuple

from trello_model.board import Board

List = namedtuple('List', ['id', 'name', 'cards'])
Card = namedtuple('Card', ['id', 'name', 'description', 'comments', 'voters'])
Comment = namedtuple('Comment', ['text', 'author'])


class TrelloExtractor:
    def __init__(self, trello):
        self.trello = trello
        self.members = {}

    def extract(self, board_id):
        name = self.trello.boards.get(board_id)['name'].encode('utf-8')
        lists = []
        for trello_list in self.trello.boards.get_list(board_id):
            current_list = List(trello_list['id'], trello_list['name'].encode('utf-8'), [])
            for card in self.trello.lists.get_card(trello_list['id']):
                description = None if not card['desc'] \
                    else card['desc'].encode('utf-8')
                comments = [] if card['badges']['comments'] == 0 \
                    else self._retrieve_comments(card['id'])
                voters = [] if card['badges']['votes'] == 0 \
                    else self._voters_id_to_username(card['idMembersVoted'])
                current_list.cards.append(Card(card['id'],
                                               card['name'].encode('utf-8'),
                                               description,
                                               comments,
                                               voters))
            lists.append(current_list)

        return Board(name, lists)

    def _retrieve_comments(self, card_id):
        return [Comment(action['data']['text'].encode('utf-8'),
                        action['memberCreator']['fullName'])
                for action in self.trello.cards.get_action(card_id)
                if action['type'] == 'commentCard']

    def _voters_id_to_username(self, voter_ids):
        return list(map(lambda voter: self._get_member(voter)['fullName'],
                        voter_ids))

    def _get_member(self, member_id):
        if member_id in self.members:
            return self.members[member_id]
        else:
            member = self.trello.members.get(member_id)
            self.members[member_id] = member
            return member
