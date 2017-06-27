"""Module with functions for parsing the sitemap of the project
„Mathe für Nicht-Freaks“."""

# Copyright 2017 Stephan Kulla
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import requests

SITEMAP_ARTICLE_NAME = "Mathe für Nicht-Freaks: Sitemap"
WIKIBOOKS_URL = "http://de.wikibooks.org/w/index.php"

def generate_sitemap_nodes(sitemap_text):
    """Generator for all node specifications in a sitemap source code. It
    yields dictionaries of the form:

        { "code": code, "depth": depth, "children": [] }

    Thereby `code` is a string representation of the node and `depth` is a
    number corresponding to the node's depth. The higher the depth is, the
    deeper the node need to be included in the final tree.
    """
    # In MediaWiki the maximal depth of a headline is 6 (as in HTML).
    # For list elements this maximal header depth is added so that list
    # elements will always be included under a headline node.
    max_headline_depth = 6

    headline_re = re.compile(r"""(={1,%s}) # Equal signs of the headline
                                 (.*)      # code defining the node
                                 \1        # Repeatation of the equal signs
                              """ % max_headline_depth, re.X)

    list_re = re.compile(r"""([*]+) # asteriks of a list element
                             (.*)   # code defining a sitemap node
                          """, re.X)

    for line in sitemap_text.splitlines():
        for regex, depth_start in ((headline_re, 0),
                                   (list_re, max_headline_depth)):
            match = regex.fullmatch(line.strip())

            if match:
                yield {
                    "code": match.group(2).strip(),
                    "depth": depth_start + len(match.group(1)),
                    "children": []
                }

def insert_node(node, new_node):
    """Inserts the node `new_node` in the tree `node` at the right position
    regarding to the attribute `depth` of `node`."""
    if node["children"] and new_node["depth"] > node["children"][-1]["depth"]:
        insert_node(node["children"][-1], new_node)
    else:
        node["children"].append(new_node)

def parse_sitemap_node_codes(node):
    """Returns a new tree where the `code` attributes are parsed. The nodes of
    the new tree contain a `name` and a `link` attribute. The `name` attribute
    corresponds to the name of the node which shall be appear in the table of
    contents. The `link` corresponds to the title of the Wikibooks page the
    node points to. In case there is no article behind the node, the attribute
    `link` is `None`.
    """

    # Delete `{{Symbol|..%}}` at the end of the code
    code = re.sub(r"\s+\{Symbol\|\d+%\}\}\s+\Z", "", node["code"])

    # Parse links of the form `[[<title>|<name>]]`
    match = re.match(r"""
        \[\[      # [[
        ([^|\]]+) # title of the page on Wikibooks
        \|        # |
        ([^|\]]+) # name of the node in toc
        \]\]      # ]]
    """, code, re.X)

    if match:
        link = match.group(1)
        name = match.group(2)
    else:
        name = code
        link = None

    return {
        "link": link,
        "name": name,
        "children": [parse_sitemap_node_codes(x) for x in node["children"]]
    }


def parse_sitemap(sitemap_text):
    """Parse the sitemap and returns a JSON object representing it.

    Arguments:
        sitemap_text -- content of the sitemap (a string)
    """
    root = {"children":[], "depth":0, "code": "Mathe für Nicht-Freaks"}

    for node in generate_sitemap_nodes(sitemap_text):
        insert_node(root, node)

    return parse_sitemap_node_codes(root)

def get_sitemap():
    """Returns the sitemap of the project „Mathe für Nicht-Freaks“."""
    params = {"action": "raw", "title": SITEMAP_ARTICLE_NAME}
    sitemap_text = requests.get(WIKIBOOKS_URL, params=params).text

    return parse_sitemap(sitemap_text)
