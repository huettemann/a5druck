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


# Get orientation
landscape = False
if round(sourcepage.mediabox.width) == PaperSize.A5.width and round(sourcepage.mediabox.height) == PaperSize.A5.height:
    # print("source no landscape")
    landscape = False
elif round(sourcepage.mediabox.width) == PaperSize.A5.height and round(sourcepage.mediabox.height) == PaperSize.A5.width:
    # print("source is landscape")
    landscape = True
else:
    print("No a5 Paper given ... quitting")
    quit()


# Create a destination file, and add a blank page to it
writer = PdfWriter()
if landscape:
    destpage = writer.add_blank_page(width=PaperSize.A4.width, height=PaperSize.A4.height)
    for row in range(2):
        destpage.merge_transformed_page(sourcepage, 
                                        Transformation().translate(
                                            0 * sourcepage.mediabox.width,
                                            row * sourcepage.mediabox.height,
                                            ),
                                        )
else:
    destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
    for row in range(2):
        destpage.merge_transformed_page(sourcepage, 
                                        Transformation().translate(
                                            row * sourcepage.mediabox.width,
                                            0 * sourcepage.mediabox.height,
                                            # 0 * sourcepage.mediabox.height,
                                            # row * sourcepage.mediabox.width,
                                            ),
                                        )


# Write file
with open(filename + "_druck.pdf", "wb") as fp:
    writer.write(fp)
