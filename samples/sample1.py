# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from sets import Set
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from ingredientsdetector import IngredientsDetector

html_doc = """
<div id="ingredients" class="module bordered module padded">
                                                <h2>Ingredients</h2>
                                                                                                        <dl id="stages">
                                                                                                                                <dt class="stage-title">For the marinade</dt>
                                                                        <dd>
                                                                                                                                        <ul>
                                                                                                                                    <li><p class="ingredient">large knob fresh <a href="/food/ginger" class="name food">ginger</a>, peeled and roughly chopped </p></li>
                                                                                                                                    <li><p class="ingredient">2-3 <a href="/food/garlic" class="name food">garlic</a> cloves, peeled and finely chopped</p></li>
                                                                                                                                    <li><p class="ingredient">2-4 green chillies, cut in half with the stalk, <a href="/food/seed" class="name food">seeds</a> and membranes removed </p></li>
                                                                                                                                    <li><p class="ingredient">1 tsp <a href="/food/salt" class="name food">salt</a>, or to taste</p></li>
                                                                                                                                    <li><p class="ingredient">1 tsp <a href="/food/garam_masala" class="name food">garam masala</a></p></li>
                                                                                                                                    <li><p class="ingredient">1 tbsp <a href="/food/lemon_juice" class="name food">lemon juice</a></p></li>
                                                                                                                                    <li><p class="ingredient">2 tbsp <a href="/food/oil" class="name food">oil</a></p></li>
                                                                                                                                        </ul>
                                                                                                                                </dd>
                                                                                                                                        <dt class="stage-title">For the chicken</dt>
                                                                        <dd>
                                                                                                                                        <ul>
                                                                                                                                    <li><p class="ingredient">800g/1lb 12oz <a href="/food/chicken" class="name food">chicken</a> pieces, skinned and pricked all over with a fork</p></li>
                                                                                                                                    <li><p class="ingredient">3 tbsp <a href="/food/vegetable_oil" class="name food">vegetable oil</a> </p></li>
                                                                                                                                    <li><p class="ingredient">¼ tsp <a href="/food/salt" class="name food">salt</a> </p></li>
                                                                                                                                    <li><p class="ingredient">¼ tsp freshly ground <a href="/food/black_pepper" class="name food">black pepper</a> </p></li>
                                                                                                                                    <li><p class="ingredient">½ tsp ground <a href="/food/cumin" class="name food">cumin</a></p></li>
                                                                                                                                    <li><p class="ingredient">4 slices white bread, processed to crumbs in a food processor</p></li>
                                                                                                                                    <li><p class="ingredient">1-2 large free-range <a href="/food/egg" class="name food">eggs</a>, beaten</p></li>
                                                                                                                                    <li><p class="ingredient">1 <a href="/food/lemon" class="name food">lemon</a>, to serve</p></li>
                                                                                                                                        </ul>
                                                                                                                                </dd>
                                                                                                                        </dl>
                                                                                        </div>
"""

if __name__ == '__main__':
    detector = IngredientsDetector()
    print detector.extract(html_doc)
