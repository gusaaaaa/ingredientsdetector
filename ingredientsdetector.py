# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from collections import defaultdict
from sets import Set
from operator import itemgetter

class IngredientsDetector(object):
    def __init__(self):
        quantity = ["\d+", "\d+[\.-]\d+", 
                    "(?:<sup>)?\d+(?:</sup>)?(?:/|&frasl;|&\#8260;|&\#x2044;)(?:<sub>)?\d+(?:</sub>)?",
                    "[½,⅓,¼,⅕,⅙,⅐,⅛,⅑,⅒,¾]",
                    "(?:&frac14;|&frac12;|&frac34;)"]
        units = ["teaspoon", "t", "tsp",
                 "tablespoon", "tbl", "tbs", "tbsp", 
                 "fluid ounce", "fl oz",
                 "gill",
                 "cup", "c",
                 "pint", "p", "pt", "fl pt",
                 "quart", "q", "qt", "fl qt",
                 "gallon", "g", "gal",
                 "milliliter", "millilitre", "ml", "cc",
                 "liter", "litre", "l",
                 "deciliter", "decilitre", "dl",
                 "pound", "lb", "\#",
                 "ounce", "oz",
                 "microgram", "microgramme", "mcg", "ug", "μg",
                 "milligram", "milligramme", "mg",
                 "gram", "gramme", "g",
                 "kilogram", "kilogramme", "kg",
                 "millimeter", "millimetre", "mm",
                 "centimeter", "centimetre", "cm",
                 "meter", "metre", "m",
                 "inch", "in", "\""] # source: http://en.wikibooks.org/wiki/Cookbook:
        pattern = r"^(?:%s)\.?\s*(?:%s)(?:s|es)?\s+.+$" % ("|".join(quantity), "|".join(units))
        self.__instruction_pattern = re.compile(pattern, re.IGNORECASE)

    def extract(self, html):
        soup = BeautifulSoup(html)
        self.__add_x_attributes(soup)
        result = self.__find_related(soup.find_all(self.__instruction_line))
        self.__remove_x_attributes(soup)
        return result

    def __add_x_attributes(self, soup):
        uid = 0
        for tag in soup.find_all(True):
            tag["xuid"] = uid
            uid += 1

    def __remove_x_attributes(self, soup):
        for tag in soup.find_all(True):
            del tag["xuid"]
            if tag.has_key("xexclude"):
                del tag["xexclude"]

    def __instruction_line(self, tag):
        if tag.has_key("xexclude"):
            return False
        w = []

        for child in tag.contents:
            if isinstance(child, NavigableString):
                s = unicode(child).strip()
                if s:
                    w.append(unicode(child))
            else:
                if child.name in ['b', 'big', 'i', 'small', 'tt',
                                  'abbr', 'acronym', 'cite', 'code',
                                  'dfn', 'em', 'kbd', 'strong',
                                  'samp', 'var', 'a', 'bdo', 'br',
                                  'img', 'map', 'object', 'q',
                                  'script', 'span', 'sub', 'sup',
                                  'button', 'input', 'label',
                                  'select', 'textarea']:
                    for subchild in child.contents:
                        s = unicode(subchild).strip()
                        if s:
                            w.append(s)

        text = "".join(" ".join(w).strip().splitlines())
        result = self.__instruction_pattern.match(text)
        if result:
            for descendant in tag.find_all(True):
                descendant["xexclude"] = True

        return result

    def __is_related(self, tag1, tag2, l=0):
        if tag1.name != tag2.name:
            return False
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
                result = self.__is_related(tag1, tag2)
                if result:
                    (p, level) = result
                    k = p.__hash__()
                    related_children[k].add(tag1)
                    related_children[k].add(tag2)
                    collected_parents[k] = (p, level)
        result = []
        already_processed = Set()
        for item in sorted(collected_parents.items(), key=itemgetter(1), reverse=True):
            k = item[0]
            tags = []
            for tag in related_children[k]:
                if not tag in already_processed:
                    tags.append(tag)
                    already_processed.add(tag)
            if tags:
                all_children = collected_parents[k][0].find_all(recursive=False)
                result.append((collected_parents[k][0], tags, len(tags) / float(len(all_children))))
        return result
