class Transformer:
    @staticmethod
    def transform(transformer, board):
        transformer.board_begin(board.get_name())
        for board_list in board.get_lists():
            transformer.list_begin(board_list.name)
            for card in board_list.cards:
                transformer.card(card.name)
                if card.description is not None:
                    transformer.card_description(card.description)
                if len(card.comments) > 0:
                    for comment, author in card.comments:
                        transformer.card_comment(comment, author)
                if len(card.voters) > 0:
                    transformer.card_votes(card.voters)
            transformer.list_end()
        transformer.board_end()

        return "\n".join(transformer.get_output())
