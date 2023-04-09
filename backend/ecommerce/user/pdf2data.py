import fitz
import io
import re
from PyPDF2 import PdfReader
from PIL import Image


class PDFData:

    def __init__(self, pdf):
        self.file = r"E:\New folder (2)\Projects\Django\eCommerce\backend\ecommerce\media" + f"\{pdf}"

    def get_data_from_pdf(self):
        pdf_file = fitz.open(self.file)
        # iterate over PDF pages
        for page_index in range(len(pdf_file)):
            # get the page itself
            page = pdf_file[page_index]
            # get image list
            text = page.get_text()
            image_list = page.get_images()
            # printing number of images found in this page
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(image_list, start=1):
                # get the XREF of the image
                xref = img[0]
                # extract the image bytes
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                # get the image extension
                image_ext = base_image["ext"]
                # load it to PIL
                image = Image.open(io.BytesIO(image_bytes))
                # save it to local disk
                # image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))

        pdfReader = PdfReader(self.file)

        # Extract and concatenate each page's content
        text = ''
        for i in range(0, len(pdfReader.pages)):
            # creating a page object
            pageObject = pdfReader.pages[i]
            # extracting text from page
            text += pageObject.extract_text()

        # print(text)
        return {
            "National ID ": next(iter(re.findall("National ID (.*?)\n", text)), ''),
            "Name(English) ": next(iter(re.findall("Name\(English\) (.*?)\n", text)), ''),
            "Name(Bangla) ": next(iter(re.findall("Name\(Bangla\) (.*?)\n", text)), ''),
            "Pin ": next(iter(re.findall("Pin (.*?)\n", text)), ''),
            "Father Name ": next(iter(re.findall("Father Name (.*?)\n", text)), ''),
            "Mother Name ": next(iter(re.findall("Mother Name (.*?)\n", text)), ''),
            "Birth Place ": next(iter(re.findall("Birth Place (.*?)\n", text)), ''),
            "Date of Birth ": next(iter(re.findall("Date of Birth (.*?)\n", text)), ''),
            "Blood Group ": next(iter(re.findall("Blood Group (.*?)\n", text)), ''),
            "Village/R oad ": next(iter(re.findall("Village/R oad (.*?)\n", text)), ''),
            "Upozila ": next(iter(re.findall("Upozila ([^A].*?) ", text)), ''),
            "Mouza/Moholla ": next(iter(re.findall("Mouza/Moholla ([^A].*?)\n", text)), ''),
            "Postal Code ": next(iter(re.findall("Postal Code (.*?)\n", text)), ''),
            "District ": next(iter(re.findall("District (.*?)\n", text)), ''),
        }

        print("National ID ", re.findall("National ID (.*?)\n", text)[0])
        print("Name(English) ", re.findall("Name\(English\) (.*?)\n", text)[0])
        print("Name(Bangla) ", re.findall("Name\(Bangla\) (.*?)\n", text)[0])
        print("Pin ", re.findall("Pin (.*?)\n", text)[0])
        print("Father Name ", re.findall("Father Name (.*?)\n", text)[0])
        print("Mother Name ", re.findall("Mother Name (.*?)\n", text)[0])
        print("Birth Place ", re.findall("Birth Place (.*?)\n", text)[0])
        print("Date of Birth ", re.findall("Date of Birth (.*?)\n", text)[0])
        print("Blood Group ", next(iter(re.findall("Blood Group (.*?)\n", text)), ''))
        print("Village/R oad ", next(iter(re.findall("Village/R oad (.*?)\n", text)), ''))
        print("Upozila ", next(iter(re.findall("Upozila (.*?)\n", text)[0]), ''))
        print("Mouza/Moholla ", re.findall("Mouza/Moholla (.*?)\n", text)[0])
        print("Postal Code ", re.findall("Postal Code (.*?)\n", text)[0])
        print("District ", re.findall("District (.*?)\n", text)[0])
