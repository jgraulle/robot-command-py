#!/bin/bash

set -ex

mkdir -p output

pdflatex -interaction nonstopmode -output-directory output main.tex
bibtex output/main
pdflatex -interaction nonstopmode -output-directory output main.tex
pdflatex -interaction nonstopmode -output-directory output main.tex
