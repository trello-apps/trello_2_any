from trello_model import TrelloExtractor
from trello_model.transformer import Transformer
from trello_transformers import ConfluenceTransformer, MarkdownTransformer, AsciiDocTransformer


class TrelloConverter:
    def __init__(self, trello, board_id):
        extraction = TrelloExtractor(trello)
        self.board = extraction.extract(board_id)

    def to(self, target):
        return Transformer.transform(_find_transformer(target), self.board)

    def to_template(self, template):
        print(template.render({'title': self.board.get_name(),
                               'board_lists': self.board.get_lists()}))


def _find_transformer(target):
    if target == Target.CONFLUENCE:
        return ConfluenceTransformer()
    elif target == Target.MARKDOWN:
        return MarkdownTransformer()
    elif target == Target.ASCIIDOC:
        return AsciiDocTransformer()
    else:
        raise ValueError('Invalid target value ' + target)


class Target:
    CONFLUENCE = 1
    MARKDOWN = 2
    ASCIIDOC = 3
