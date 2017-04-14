from transformer import Transformer
from trello_token import get_auth
from trello_model import TrelloBoard

from secrets.api import TRELLO_BOARD_ID


class AsciiDocTransformer(Transformer):
    def transform_board_name(self, name):
        return "{}\n{}".format(name, "=" * len(name))

    def transform_list_name(self, name):
        return "{}\n{}".format(name, '-' * len(name))

    def transform_card_name(self, name):
        return "* {}".format(name)

    def transform_card_comment(self, comment, author):
        return "** comment: {} by {}".format(comment, author)

    def transform_card_votes(self, voters):
        return "** votes: {} by {}".format(len(voters), voters)


if __name__ == '__main__':
    auth = get_auth()
    trello_board = TrelloBoard(TRELLO_BOARD_ID, auth)
    trello_board.apply_transformer(AsciiDocTransformer())
