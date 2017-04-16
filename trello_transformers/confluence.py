from .transformer import Transformer


class ConfluenceTransformer(Transformer):
    def transform_board_name(self, name):
        return "h1. {}".format(name)

    def transform_list_name(self, name):
        return "{panel:title=" + name + "}"

    def transform_card_name(self, name):
        return "* {}".format(name)

    def transform_card_comment(self, comment, author):
        return "** comment by {}: {}".format(author, comment)

    def transform_card_votes(self, voters):
        return "** {} votes by: {}".format(len(voters), ", ".join(voters))
