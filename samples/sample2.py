# -*- coding: utf-8 -*-
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from ingredientsdetector import IngredientsDetector

import urllib

if __name__ == '__main__':
    detector = IngredientsDetector()
    sites = ["http://allrecipes.com/Recipe/Lemony-Quinoa/Detail.aspx",
             "http://www.bbc.co.uk/food/recipes/ovenfriedchillichick_86437",
              "http://www.foodnetwork.com/recipes/sandra-lee/slow-cooker-short-ribs-recipe/index.html" # bug in BeautifulSoup,
             "http://www.food.com/recipe/blueberry-pancakes-42041",
             "http://www.taste.com.au/recipes/30923/miso+glazed+fish+with+sesame+brown+rice+salad",
             "http://www.bettycrocker.com/recipes/banana-bread/51427396-6764-4b0a-a73a-78c683c703d2",
             "http://www.thejoykitchen.com/recipe/dark-chocolate-truffles-liqueur",
             "http://www.gourmet.com/food/gourmetlive/2011/062911/the-founding-father-mac-and-cheese"
            ]
    for site in sites:
        print "========================="
        print "Ingredients for %s" % (site)
        print "========================="
        html = urllib.urlopen(site).read()
        result = detector.extract(html)
        for item in result:
            if item[2] >= 0.25:
                for tag in item[0].find_all(recursive=False):
                    print "* %s" % (" ".join(tag.get_text().splitlines()))
