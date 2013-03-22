import re
from bs4 import BeautifulSoup
from collections import defaultdict
from sets import Set

class IngredientsDetector(object):
    def __init__(self):
        self.__instruction_pattern = re.compile(r"\d+.+")

    def extract(self, html):
        soup = BeautifulSoup(html)
        result = self.__find_related(soup.find_all(text=self.__instruction_line))
        return result

    def __instruction_line(self, tag):
        return self.__instruction_pattern.match(tag)

    def __is_related(self, tag1, tag2, l=0):
        p1 = tag1.find_parent()
        p2 = tag2.find_parent()
        if p1 is None or p2 is None:
            return False
        elif p1 == p2:
            return (p1, l)
        else:
            return self.__is_related(p1, p2, l+1)

    def __find_related(self, tags):
        # collect all related tags
        related_children = defaultdict(set)
        collected_parents = defaultdict(list)
        i = 0
        for tag1 in tags:
            i = i+1
            for tag2 in tags[i:]:
                (p, level) = self.__is_related(tag1, tag2)
                if p:
                    k = p.__hash__()
                    related_children[k].add(tag1)
                    related_children[k].add(tag2)
                    collected_parents[k] = (p, level)

        result = []
        already_processed = Set()
        for k in collected_parents:
            tags = []
            for tag in related_children[k]:
                if not tag in already_processed:
                    tags.append(tag)
                    already_processed.add(tag)
            if tags:
                all_children = collected_parents[k][0].find_all(recursive=False)
                result.append((collected_parents[k][0], tags, len(tags) / float(len(all_children))))
        return result
