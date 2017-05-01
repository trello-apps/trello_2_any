from collections import namedtuple

List = namedtuple('List', ['id', 'name', 'cards'])
Card = namedtuple('Card', ['id', 'name', 'comments', 'voters'])
Comment = namedtuple('Comment', ['text', 'author'])


class TrelloExtraction:
    def __init__(self, trello, board_id):
        self.board = []
        self.name = 'NA'
        # for test purposes
        if trello is not None:
            self.name = trello.boards.get(board_id)['name']
            for trello_list in trello.boards.get_list(board_id):
                current_list = List(trello_list['id'], trello_list['name'], [])
                for card in trello.lists.get_card(trello_list['id']):
                    comments = [] if card['badges']['comments'] == 0 \
                        else self._retrieve_comments(trello, card['id'])
                    voters = [] if card['badges']['votes'] == 0 \
                        else self._voters_id_to_username(trello,
                                                         card['idMembersVoted'])
                    current_list.cards.append(Card(card['id'],
                                                   card['name'],
                                                   comments,
                                                   voters))
                self.board.append(current_list)
        else:
            print("TrelloApi is None, no information will be retrieved from \
Trello, your model is empty!")

    def _retrieve_comments(self, trello, card_id):
        return [Comment(action['data']['text'],
                        action['memberCreator']['fullName'])
                for action in trello.cards.get_action(card_id)
                if action['type'] == 'commentCard']

    def _voters_id_to_username(self, trello, voters):
        return list(map(lambda voter: trello.members.get(voter)['fullName'],
                        voters))

    def apply_transformer(self, transformer):
        output = []
        output.append(transformer.transform_board_name(self.name))
        for board_list in self.board:
            output.append(transformer.transform_list_name(board_list.name))
            for card in board_list.cards:
                output.append(transformer.transform_card_name(card.name))
                if len(card.comments) > 0:
                    for comment, author in card.comments:
                        output.append(transformer.transform_card_comment(
                                      comment,
                                      author))
                if len(card.voters) > 0:
                    output.append(transformer.transform_card_votes(card.voters))
        return "\n".join(output)

    def apply_template(self, template):
        print(template.render({'title': self.name,
                               'board_lists': self.board}))
