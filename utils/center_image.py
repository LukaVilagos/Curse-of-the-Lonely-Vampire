from constants.backgrounds import background

def center_image_vertically(image, scale):
    return (background.get_width() / 2) - (image.get_width() * scale / 2)

def center_image_horizontally(image, scale):
    return (background.get_height() / 2) - (image.get_height() * scale / 2)