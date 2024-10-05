
from dataclasses import dataclass
import PIL
import PIL.Image

import xcftools


@dataclass
class PlacedImage:
    img: PIL.Image
    x: int
    y: int
    layer: xcftools.Layer


def place_images(layers, max_width, pad=1):
    '''Packs the list of images into a box, given it's maximum width, expanding
    the height as necessary to fit all images. This returns a list of placed
    images.'''

    # First decide on how to layout the images
    def _get_all_layers(layers):
        if not layers:
            return []
        all_layers = layers
        for layer in layers:
            all_layers.extend(_get_all_layers(layer.layers))
        return all_layers

    def _get_images(layers):
        if not layers:
            return []
        images = [
            layer.image
            for layer in layers
        ]
        for layer in layers:
            images.extend(_get_images(layer.layers))
        return images

    layers = _get_all_layers(layers)
    img_list = _get_images(layers)

    x = pad
    y = pad
    line_height = 0
    dest_width = 0
    placed_imgs = []
    for layer, img in zip(layers, img_list):
        # Place the images horizontally until they won't fit anymore, then
        # skip down and start a new line.
        if (max_width > 0 and x + pad + img.size[0] >= max_width):
            x = pad
            y += pad + line_height
            line_height = 0
            assert(img.size[0] + 2*pad < max_width)

        placed_imgs.append(PlacedImage(img, x, y, layer))
        x += pad + img.size[0]
        dest_width = max(dest_width, x)
        line_height = max(line_height, img.size[1])

    dest_height = y + pad + line_height
    return placed_imgs, dest_width, dest_height


def pack_images(layers, max_width):
    '''Pack the list of PIL images into a new image, being somewhat space
    efficient. This returns the new image, and a list of locations.'''

    assert layers, 'there are no images to pack'

    placed_imgs, dest_width, dest_height = place_images(layers, max_width)

    # Now paste everything into a big image map
    dest_img = PIL.Image.new('RGBA', (dest_width, dest_height))
    for placed in placed_imgs:
        dest_img.paste(placed.img, (placed.x, placed.y))

    return dest_img, placed_imgs
