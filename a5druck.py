#!/usr/bin/python3

from pypdf import PdfReader, PdfWriter, Transformation, PaperSize
import sys, argparse


# CLI
parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()
file = args.file
filename = file.replace('.pdf', '')


# Read source file
reader = PdfReader(file)
sourcepage = reader.pages[0]


# Create a destination file, and add a blank page to it
writer = PdfWriter()
destpage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)


# Copy source page to destination page, two times
for row in range(2):
    destpage.merge_transformed_page(sourcepage, 
                                    Transformation().translate(
                                        0 * sourcepage.mediabox.width,
                                        row * sourcepage.mediabox.height,
                                        ),
                                    )


# Write file
with open(filename + "_druck.pdf", "wb") as fp:
    writer.write(fp)
