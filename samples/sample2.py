# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from ingredientsdetector import IngredientsDetector

import urllib

if __name__ == '__main__':
    detector = IngredientsDetector()
    html = urllib.urlopen("http://allrecipes.com/Recipe/Lemony-Quinoa/Detail.aspx").read()
    result = detector.extract(html)
    for item in result:
        if item[2] > 0.25:
            print item
            print "========================="
