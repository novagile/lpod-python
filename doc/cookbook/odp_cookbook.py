# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Itaapy, ArsAperta, Pierlis, Talend

# Import from lpod
from lpod.document import odf_new_document_from_type
from lpod.draw_page import odf_create_draw_page
from lpod.frame import odf_create_text_frame, odf_create_image_frame
from lpod.paragraph import odf_create_paragraph

PPC = 72 * 2.54


# helper function
def get_thumbnail_file(filename):
    from PIL import Image
    from cStringIO import StringIO

    im = Image.open(filename)
    im.thumbnail((300, 400), Image.ANTIALIAS)
    filedescriptor = StringIO()
    im.save(filedescriptor, 'JPEG', quality=80)
    filedescriptor.seek(0)
    return filedescriptor, (im.size[0] / PPC), (im.size[1] / PPC)



# Creation of the document
document = odf_new_document_from_type('presentation')
content = document.get_xmlpart('content')
body = content.get_body()

# The document already contains a page
page = content.get_draw_page_by_position(1)

# Add a frame with a text box
text_element = odf_create_paragraph(u'First Slide')
draw_textframe1 = odf_create_text_frame(text_element,
                                        size=('5cm', '100mm'),
                                        position=('3.5cm', '30.6mm'))
page.append_element(draw_textframe1)

# If first arg is text a paragraph is created
draw_textframe2 = odf_create_text_frame(u"Noël",
                                        size=('5cm', '100mm'),
                                        position=('20cm', '14cm'))
page.append_element(draw_textframe2)

# Add an image frame from a file name
local_uri = document.add_file(u'images/zoé.jpg')
draw_imageframe1 = odf_create_image_frame(local_uri,
                                          size=('6cm', '24.2mm'),
                                          position=('1cm', '10cm'))
page.append_element(draw_imageframe1)

# Add an image frame from a file descriptor
filedescriptor, width, height = get_thumbnail_file(u'images/zoé.jpg')
local_uri = document.add_file(filedescriptor)
draw_imageframe2 = odf_create_image_frame(local_uri,
                                          size=('%scm' % width,
                                                '%scm' % height),
                                          position=('12cm', '2cm'))
page.append_element(draw_imageframe2)

# Add the page to the body
body.append_element(page)

# Get a new page, page2 copy of page1
page2 = page.clone()
page2.set_page_name(u'Page 2')
head = content.get_paragraph_by_content(u'First', context=page2)
head.set_text(u'Second Slide')
body.append_element(page2)

# Save
document.save('presentation.odp', pretty=True)
