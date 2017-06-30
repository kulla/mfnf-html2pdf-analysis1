"""Script which creates a Makefile for making a PDF of the book „Analysis 1“ of
the project „Mathe für Nicht-Freaks“."""

from itertools import chain
from urllib.parse import quote
from sitemap import get_sitemap

def iter_nodes(sitemap_node):
    """Iterate over all nodes of `sitemap_node` using depth first."""
    yield sitemap_node

    yield from chain(*map(iter_nodes, sitemap_node["children"]))

def run_script():
    """Runs this script."""
    book = get_sitemap()["children"][2]

    nodes = [x for x in iter_nodes(book) if x["link"]]
    links = ["http://de.wikibooks.org/w/index.php?printable=yes&" + \
             "title=" + quote(x["link"])
             for x in nodes]
    targets = ["out/page%04d.pdf" % x for x in range(len(links))]

    for link, target in zip(links, targets):
        print(link + " " + target)

if __name__ == "__main__":
    run_script()
