import unittest

from trello_model import TrelloExtraction
from trello_model import Card, List, Comment

from trello_transformers import MarkdownTransformer, AsciiDocTransformer


class TestTransformer(unittest.TestCase):
    def setUp(self):
        self.extraction = TrelloExtraction(None, None)
        cards = [Card('1', 'card 1', [], ['person1']),
                 Card('2', 'card 2',
                      [Comment('text comment', 'person1'),
                       Comment('text comment 2', 'person2')],
                      ['person1', 'person2', 'person3 lastname'])]
        self.extraction.board.append(List('1', 'sample_list1', cards))

    def tearDown(self):
        self.board = None

    def test_markdown_transformation_of_board(self):
        output = self.extraction.apply_transformer(MarkdownTransformer())
        expected_output = '''# NA
## sample_list1
- card 1
    - 1 vote(s), by: person1
- card 2
    - comment by person1: text comment
    - comment by person2: text comment 2
    - 3 vote(s), by: person1, person2, person3 lastname'''
        self.assertEqual(output, expected_output)

    def test_asciidoc_transformation_of_board(self):
        output = self.extraction.apply_transformer(AsciiDocTransformer())
        expected_output = '''NA
==
sample_list1
------------
* card 1
** 1 votes by: person1
* card 2
** comment by person1: text comment
** comment by person2: text comment 2
** 3 votes by: person1, person2, person3 lastname'''
        self.assertEqual(output, expected_output)
