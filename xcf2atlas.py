#!/usr/bin/env python3
#
# xcf2atlas - Convert XCF images into an image atlas
# Copyright (C) 2017  Peter Rogers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import PIL
import PIL.Image
import sys
import os
import argparse
from collections import namedtuple

import xcftools

def place_images(img_list, max_width, pad=1):
    """Packs the list of images into a box, given it's maximum width, expanding
    the height as necessary to fit all images. This returns a list of placed
    images."""
    PlacedImage = namedtuple('PlacedImage', ('img', 'x', 'y'))

    x = pad
    y = pad
    line_height = 0
    dest_width = 0
    placed_imgs = []
    for img in img_list:
        # Place the images horizontally until they won't fit anymore, then
        # skip down and start a new line.
        if (x + pad + img.size[0] >= max_width):
            x = pad
            y += pad + line_height
            line_height = 0
            assert(img.size[0] + 2*pad < max_width)

        placed_imgs.append(PlacedImage(img, x, y))
        x += pad + img.size[0]
        dest_width = max(dest_width, x)
        line_height = max(line_height, img.size[1])

    #dest_width += pad
    dest_height = y + pad + line_height
    return placed_imgs, dest_width, dest_height

def pack_images(img_list, max_width):
    """Pack the list of PIL images into a new image, being somewhat space
    efficient. This returns the new image, and a list of locations."""

    # First decide on how to layout the images
    placed_imgs, dest_width, dest_height = place_images(img_list, max_width)

    # Now paste everything into a big image map
    dest_img = PIL.Image.new("RGBA", (dest_width, dest_height))
    for placed in placed_imgs:
        dest_img.paste(placed.img, (placed.x, placed.y))

    return dest_img, ((placed.x, placed.y) for placed in placed_imgs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build an image atlas from a collection of XCF files')
    parser.add_argument('--image', dest="image_file", nargs=1, required=True)
    parser.add_argument('--json', dest="json_file", nargs=1, required=True)
    parser.add_argument('--max-width', dest="max_width", 
                        nargs=1, type=int, default=[256])
    parser.add_argument('src', nargs='+')
    args = parser.parse_args(sys.argv[1:])

    for src in args.src:
        if not os.path.exists(src):
            raise FileNotFoundError(src)

    sprite_names = {}
    all_layers = []
    all_images = []
    for src in args.src:
        layers = xcftools.get_layer_info(src)
        all_layers += layers
        all_images += [
            xcftools.extract_layer(src, layer.name)
            for layer in layers
        ]
        base_name = os.path.splitext(os.path.basename(src))[0]
        sprite_names.update({
            layer : base_name + "_" + layer.name
            for layer in layers
        })

    dest_json_path = args.json_file[0]
    dest_image_path = args.image_file[0]

    # Pack and save the image
    dest_img, positions = pack_images(all_images, args.max_width[0])
    dest_img.save(dest_image_path)

    # Write out the json
    json_data = {
        'meta' : {
            'format' : 'RGBA8888',
            'image' : os.path.basename(dest_path),
            'app' : 'xcf2atlas',
            'scale' : '1',
            'verison' : '1',
            'size' : {
                'w' : dest.size[0],
                'h' : dest.size[1],
            }
        },
        'frames' : {
            sprite_names[layer] : {
                'frame' : {
                    'x' : pos[0], 
                    'y' : pos[1], 
                    'w' : layer.w, 
                    'h' : layer.h
                },
                'rotated' : False,
                'trimmed' : False,
                'spriteSourceSize' : {
                    'x' : 0, 
                    'y' : 0, 
                    'w' : layer.w, 
                    'h' : layer.h
                },
                'sourceSize' : {'w' : layer.w, 'h' : layer.h},
                'pivot' : {'x' : 0.5, 'y' : 0.5}
            }
            for layer, pos in zip(all_layers, positions)
        }
    }
    json.dump(json_data, open(dest_json_path, "w"))
