import unittest
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))

import re
from bs4 import BeautifulSoup

from ingredientsdetector import IngredientsDetector

class IngredientsDetectorTest(unittest.TestCase):
    def setUp(self):
        self.subject = IngredientsDetector()

    def test_should_not_extract_lists_with_less_than_two_items(self):
        html = """
        <div>
            <p>1 banana</p>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 0)

    def test_should_extract_all_tags_matching_the_pattern(self):
        html = """
        <div>
            <p>1 banana</p>
            <p>1 pera</p>
            <p>3 ciruelas</p>
        </div>
        """
        s = self.subject.extract(html)

        self.assertEqual(len(s), 1)
        self.assertEqual(len(s[0][1]), 3)

    def test_should_extract_the_minimum_common_ancestor(self):
        html = """
        <div>
            <ul>
                <li><span>1 banana</span></li>
                <li><span>1 pera</span></li>
                <li><span>3 ciruelas</span></li>
            </ul>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(s[0][0].name, "ul")

    def test_should_group_by_the_closest_ancestor(self):
        html = """
        <div>
            <div>
                <p>1 banana</p>
                <p>2 manzanas</p>
            </div>
            <div>
                <p>1 sandia</p>
                <p>3 ciruelas</p>
                <p>1 pera</p>
            </div>
        </div>
        """
        s = self.subject.extract(html)

        self.assertEqual(len(s), 2)
        self.assertEqual(len(s[0][1]), 2)
        self.assertEqual(len(s[1][1]), 3)

    def test_should_return_a_confidence_factor(self):
        html = """
        <div>
            <ul>
                <li><span>1 banana</span></li>
                <li><span>1 pera</span></li>
                <li><span>manteca</span></li>
                <li><span>ketchup</span></li>
            </ul>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(s[0][2], 0.5)

if __name__ == '__main__':
        unittest.main()
