#!/bin/bash

set -ex

mkdir -p output

pdflatex -interaction nonstopmode -output-directory output main.tex
