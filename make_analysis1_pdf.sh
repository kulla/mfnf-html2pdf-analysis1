#!/bin/sh

test -d out || mkdir out
python create_arguments.py | wkhtmltopdf --read-args-from-stdin
pdfjoin --outfile "out/analysis1.pdf"  out/page*pdf
