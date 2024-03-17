import os
import sys
from argparse import ArgumentParser

from pdf2docx import Converter

parser = ArgumentParser()
parser.add_argument("-p", "--pdf", type=str, help="Path to the PDF file")
parser.add_argument("-o", "--output", type=str, help="Path to the DOCX file")
parser.add_argument("-d", "--directory", type=str, required=False, help="Path to the directory to save the DOCX file")

args = parser.parse_args()

pdf_file = args.pdf
output_file = args.output
output_directory = args.directory

if not output_directory:
    output_directory = os.environ.get("HOME")

if not pdf_file:
    parser.print_usage()
    sys.exit(1)

if not output_file:
    parser.print_usage()
    sys.exit(1)


# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(output_file)  # all pages by default # type: ignore
cv.close()
