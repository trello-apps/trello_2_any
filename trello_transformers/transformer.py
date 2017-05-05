class Transformer:
    def __init__(self):
        self.output = []

    def append(self, line):
        self.output.append(line)

    def get_output(self):
        return self.output

    def board_begin(self, name):
        raise NotImplementedError()

    def board_end(self):
        raise NotImplementedError()

    def list_begin(self, name):
        raise NotImplementedError()

    def list_end(self):
        raise NotImplementedError()

    def card(self, name):
        raise NotImplementedError()

    def card_description(self, name):
        raise NotImplementedError()

    def card_comment(self, comment, author):
        raise NotImplementedError()

    def card_votes(self, voters):
        raise NotImplementedError()
