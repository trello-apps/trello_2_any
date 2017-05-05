from .transformer import Transformer


class ConfluenceTransformer(Transformer):
    def board_begin(self, name):
        self.append('h1. {}'.format(name))
        self.append('{section}')

    def board_end(self):
        self.append('{section}')

    def list_begin(self, name):
        self.append('{column}')
        self.append('{panel:title=' + name + '}')

    def list_end(self):
        self.append('{panel}')
        self.append('{column}')

    def card(self, name):
        self.append('* {}'.format(name))

    def card_description(self, name):
        self.append('** {}'.format(name))

    def card_comment(self, comment, author):
        self.append('** comment by {}: {}'.format(author, comment))

    def card_votes(self, voters):
        self.append('** {} vote(s), by: {}'.format(len(voters), ', '.join(voters)))
