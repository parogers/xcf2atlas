
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


def place_images(
    layers,
    max_width,
    include_group_images=False,
    pad=1,
):
    '''Packs the list of images into a box, given it's maximum width, expanding
    the height as necessary to fit all images. This returns a list of placed
    images.'''

    def _iter_nested_layers(layers):
        for layer in layers:
            if include_group_images or not layer.is_group:
                yield layer
            yield from _iter_nested_layers(layer.layers)

    x = pad
    y = pad
    line_height = 0
    dest_width = 0
    placed_imgs = []
    for layer in _iter_nested_layers(layers):
        # Place the images horizontally until they won't fit anymore, then
        # skip down and start a new line.
        img = layer.image
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


def pack_images(
    layers,
    max_width,
    include_group_images=False,
):
    '''Pack the list of PIL images into a new image, being somewhat space
    efficient. This returns the new image, and a list of locations.'''

    assert layers, 'there are no images to pack'

    placed_imgs, dest_width, dest_height = place_images(
        layers,
        max_width,
        include_group_images=include_group_images,
    )

    # Now paste everything into a big image map
    dest_img = PIL.Image.new('RGBA', (dest_width, dest_height))
    for placed in placed_imgs:
        dest_img.paste(placed.img, (placed.x, placed.y))

    return dest_img, placed_imgs
