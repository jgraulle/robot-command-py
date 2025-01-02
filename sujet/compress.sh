#!/bin/bash

set -ex

ls -lh output/main.pdf

ghostscript -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/printer -dNOPAUSE -dQUIET -dBATCH -sOutputFile=output/compressed.pdf output/main.pdf
mv output/compressed.pdf output/main.pdf

ls -lh output/main.pdf
