"""Script which creates a Makefile for making a PDF of the book „Analysis 1“ of
the project „Mathe für Nicht-Freaks“."""

import sys

from urllib.parse import quote
from sitemap import get_sitemap

PAGENO = 0

def create_arguments(node, output):
    """Prints the arguments for creating PDFs of the sitemap node `node` with
    the tool `wkhtmltopdf` to `output`. `page_nr` is the number of the current
    page."""
    global PAGENO

    if node["link"]:
        title = quote(node["link"])
        url = "http://de.wikibooks.org/w/index.php?printable=yes&" + \
              "title=" + title
        output.write(url + " out/page%04d.pdf\n" % PAGENO)
        PAGENO += 1

    for child in node["children"]:
        create_arguments(child, output)

def run_script():
    """Runs this script."""
    book = get_sitemap()["children"][2]

    create_arguments(book, sys.stdout)

if __name__ == "__main__":
    run_script()
