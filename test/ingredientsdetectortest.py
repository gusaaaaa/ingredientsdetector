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
            <p>1 l water</p>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 0)

    def test_should_not_extract_anything_if_items_are_not_in_the_same_level(self):
        html = """
        <div>
            <div>
                <div>
                    <p>1 l water</p>
                </div>
            </div>
            <div>
                <p>2 tsp flour</p>
            </div>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 0)

    def test_should_extract_all_tags_matching_the_pattern(self):
        html = """
        <div>
            <p>1 l water</p>
            <p>1/2 l oil</p>
            <p>3 kg salt</p>
        </div>
        """
        s = self.subject.extract(html)

        self.assertEqual(len(s), 1)
        self.assertEqual(len(s[0][1]), 3)

    def test_should_not_extract_anything_if_related_items_dont_share_tag_names(self):
        html = """
        <div>
            <p>1 l water</p>
            <div>2 tsp flour</div>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 0)

    def test_should_extract_the_minimum_common_ancestor(self):
        html = """
        <div>
            <ul>
                <li><span>1 litre of water</span></li>
                <li><span>1 lb onions</span></li>
                <li><span>3 kg chicken</span></li>
            </ul>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(s[0][0].name, "ul")

    def test_should_group_by_the_closest_ancestor(self):
        html = """
        <div>
            <div>
                <p>1 p beer</p>
                <p>2 g pepper</p>
            </div>
            <div>
                <p>1 cc sugar</p>
                <p>3 mg water</p>
                <p>1 kg meat</p>
            </div>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 2)

    def test_should_return_a_confidence_factor(self):
        html = """
        <div>
            <ul>
                <li><span>1 l water</span></li>
                <li><span>1 mg salt</span></li>
                <li><span>butter</span></li>
                <li><span>ketchup</span></li>
            </ul>
        </div>
        """
        s = self.subject.extract(html)
        self.assertEqual(s[0][2], 0.5)

    def test_should_work_with_identical_tags(self):
        html = """
         <ul>
            <li>
                <p>3 l water</p>
            </li>
            <li>
                <p>3 l water</p>
            </li>
        </ul>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 1)

    def test_should_be_tolerant_to_inline_tags(self):
        html = """
         <ul>
            <li>
                <p>3 <strong>l</strong> water</p>
                <p>2 <strong>g</strong> salt</p>
            </li>
        </ul>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 1)

    def test_should_be_tolerant_when_children_are_all_inline_tags(self):
        html = """
         <ul>
            <li>
                <p><strong>3 l</strong><span>water</span></p>
                <p><strong>2 g</strong><span>salt</span></p>
            </li>
        </ul>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 1)

    def test_should_not_process_inline_tags_when_they_match_search_criteria(self):
        html = """
         <ul>
            <li>
                <div>3 l water <strong>4 kg salt</strong></div>
                <div>2 l kerosene <strong>4 g pepper</strong></div>
            </li>
        </ul>
        """
        s = self.subject.extract(html)
        self.assertEqual(len(s), 1)
        self.assertEqual(len(s[0][1]), 2)

if __name__ == '__main__':
        unittest.main()
