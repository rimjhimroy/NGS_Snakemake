import fileinput

def fastqc_html_to_image_files(filename,content):
    import os
    import re
    import lxml
    import base64
    from lxml.html import fromstring
    # Create lxml document from string we created
    document = fromstring(content)

    # Look for all the different parts of the file
    modules = document.xpath("//div[@class='module']")

    # Put the titles and images in a dictionary
    images = {}
    for module in modules:
        paragraph = module.find('p')              # The images are contained in a p tag
        header = module.find('h2')                # The type of image can be found in the h2 header
        if paragraph is not None:                 # Skip over modules that do not contain a p tag
            image = paragraph.find('img')         # Grab the image out of the HTML
            if image is not None:                 # Skip if there is no image
                # Remove the newline form the header, and compress all double spaces to a single one
                # And add the image as an image to the dictionary
                images[((re.sub(' +', ' ',header.text_content().replace('\n', ''))))] = image.attrib['src'].split(';')[1].split(',')[1].encode()

    # Output all images from the file, with titles
    for title, image in images.items():
        file_out = os.path.splitext(os.path.basename(filename))[0]+'.'+title.lower().replace(' ', '_')+'.png'
        with open(file_out, "wb") as fh:
            fh.write(base64.decodebytes(image))

def process(fileinput):
    if fileinput.isstdin():
        print ("Can't handle stdin for now, skipping")
    else:
        filename = ""
        for line in f:
            if fileinput.isfirstline():
                # Check whether we can process the previous file
                if len(filename) != 0:
                    fastqc_html_to_image_files(filename, string)
                # Start processing a new file
                filename = fileinput.filename()
                print("Processing", filename)
                string = line
            else:
                string = string + line
        fastqc_html_to_image_files(filename, string)

with fileinput.input() as f:
    process(f)