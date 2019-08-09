from PIL import Image

filename = 'tree.png'

thumbNailSize = (128, 128)
thumb = 'thumbnail_'+filename

try:
    im = Image.open(filename)
    im.thumbnail(thumbNailSize)
    im.save(thumb, "ico")
except IOError:
    print("Cannot create thumbnail for", filename)