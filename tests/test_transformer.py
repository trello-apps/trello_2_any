import unittest

from trello_model import Card, List, Comment
from trello_model.board import Board
from trello_model.transformer import Transformer
from trello_transformers import ConfluenceTransformer, MarkdownTransformer, AsciiDocTransformer


class TestTransformer(unittest.TestCase):
    def setUp(self):
        cards = [Card('1', 'card 1', None, [], ['person1']),
                 Card('2', 'card 2', 'description',
                      [Comment('text comment', 'person1'),
                       Comment('text comment 2', 'person2')],
                      ['person1', 'person2', 'person3 lastname'])]

        self.board = Board('Board 1', [List('1', 'sample_list1', cards)])

    def test_confluence_transformation_of_board(self):
        output = Transformer.transform(ConfluenceTransformer(), self.board)
        expected_output = '''h1. Board 1
{section}
{column}
{panel:title=sample_list1}
* card 1
** 1 vote(s), by: person1
* card 2
** description
** comment by person1: text comment
** comment by person2: text comment 2
** 3 vote(s), by: person1, person2, person3 lastname
{panel}
{column}
{section}'''
        self.assertEqual(expected_output, output)

    def test_markdown_transformation_of_board(self):
        output = Transformer.transform(MarkdownTransformer(), self.board)
        expected_output = '''# Board 1
## sample_list1
- card 1
    - 1 vote(s), by: person1
- card 2
    - description
    - comment by person1: text comment
    - comment by person2: text comment 2
    - 3 vote(s), by: person1, person2, person3 lastname'''
        self.assertEqual(expected_output, output)

    def test_asciidoc_transformation_of_board(self):
        output = Transformer.transform(AsciiDocTransformer(), self.board)
        expected_output = '''Board 1
=======
sample_list1
------------
* card 1
** 1 vote(s) by: person1
* card 2
** description
** comment by person1: text comment
** comment by person2: text comment 2
** 3 vote(s) by: person1, person2, person3 lastname'''
        self.assertEqual(expected_output, output)
