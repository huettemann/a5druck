#!/usr/bin/python3

from pypdf import PdfReader, PdfWriter, Transformation, PaperSize
from pypdf.generic import AnnotationBuilder
import sys, argparse


# CLI
parser = argparse.ArgumentParser(prog='a5druck', description='duplicate a5 to printable a4', epilog='Thank you for using a5druck')
parser.add_argument("file", help="Input a5 pdf-file")
parser.add_argument('-l', '--line', help="Adds seperator-line", action='store_false')
args = parser.parse_args()
file = args.file
filename = file.replace('.pdf', '')
no_line = args.line # None -> True, -l -> False


# Read source file
reader = PdfReader(file)
sourcepage = reader.pages[0]


# Get orientation
landscape = False
sp_width = round(sourcepage.mediabox.width) 
sp_height = round(sourcepage.mediabox.height) 
if sp_width == PaperSize.A5.width and sp_height == PaperSize.A5.height:
    # print("source no landscape")
    landscape = False
elif sp_width == PaperSize.A5.height and sp_height == PaperSize.A5.width:
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
                                            0 * sp_width,
                                            row * sp_height,
                                            ),
                                        )
    if not no_line:
        annotation = AnnotationBuilder.line(
            # text="Hello World",
            rect=(0,0,0,0),
            p1=(0, sp_height),
            p2=(sp_width, sp_height),
        )
        writer.add_annotation(page_number=0, annotation=annotation)
else:
    destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
    for row in range(2):
        destpage.merge_transformed_page(sourcepage, 
                                        Transformation().translate(
                                            row * sp_width,
                                            0 * sp_height,
                                            ),
                                        )
    if not no_line:
        annotation = AnnotationBuilder.line(
            # text="Hello World",
            rect=(0,0,0,0),
            p1=(sp_width, 0),
            p2=(sp_width, sp_height),
        )
        writer.add_annotation(page_number=0, annotation=annotation)


# Write file
with open(filename + "_druck.pdf", "wb") as fp:
    writer.write(fp)
