class Transformer:
    def transform_board_name(self, name):
        raise NotImplementedError()

    def transform_list_name(self, name):
        raise NotImplementedError()

    def transform_card_name(self, name):
        raise NotImplementedError()

    def transform_card_comment(self, comment, author):
        raise NotImplementedError()

    def transform_card_votes(self, voters):
        raise NotImplementedError()
