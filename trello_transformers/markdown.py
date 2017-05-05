from .transformer import Transformer


class MarkdownTransformer(Transformer):
    def board_begin(self, name):
        self.append('# {}'.format(name))

    def board_end(self):
        pass

    def list_begin(self, name):
        self.append('## {}'.format(name))

    def list_end(self):
        pass

    def card(self, name):
        self.append('- {}'.format(name))

    def card_description(self, name):
        self.append('    - {}'.format(name))

    def card_comment(self, comment, author):
        self.append('    - comment by {}: {}'.format(author, comment))

    def card_votes(self, voters):
        self.append('    - {} vote(s), by: {}'.format(len(voters), ', '.join(voters)))
