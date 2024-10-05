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

import collections
from dataclasses import dataclass
import json
import PIL
import PIL.Image
import sys
import os
import argparse

import xcftools


@dataclass
class PlacedImage:
    img: PIL.Image
    x: int
    y: int


def place_images(img_list, max_width, pad=1):
    '''Packs the list of images into a box, given it's maximum width, expanding
    the height as necessary to fit all images. This returns a list of placed
    images.'''

    x = pad
    y = pad
    line_height = 0
    dest_width = 0
    placed_imgs = []
    for img in img_list:
        # Place the images horizontally until they won't fit anymore, then
        # skip down and start a new line.
        if (max_width > 0 and x + pad + img.size[0] >= max_width):
            x = pad
            y += pad + line_height
            line_height = 0
            assert(img.size[0] + 2*pad < max_width)

        placed_imgs.append(PlacedImage(img, x, y))
        x += pad + img.size[0]
        dest_width = max(dest_width, x)
        line_height = max(line_height, img.size[1])

    dest_height = y + pad + line_height
    return placed_imgs, dest_width, dest_height


def pack_images(layers, max_width):
    '''Pack the list of PIL images into a new image, being somewhat space
    efficient. This returns the new image, and a list of locations.'''

    # First decide on how to layout the images
    img_list = [
        layer.image
        for layer in layers
    ]
    placed_imgs, dest_width, dest_height = place_images(img_list, max_width)

    # Now paste everything into a big image map
    dest_img = PIL.Image.new('RGBA', (dest_width, dest_height))
    for placed in placed_imgs:
        dest_img.paste(placed.img, (placed.x, placed.y))

    return dest_img, ((placed.x, placed.y) for placed in placed_imgs)


def main():
    parser = argparse.ArgumentParser(
        description='Build an image atlas from a collection of XCF files'
    )
    parser.add_argument(
        '--max-width',
        dest='max_width',
        nargs=1,
        type=int,
        default=[-1]
    )
    parser.add_argument(
        '--export-image',
        dest='image_file',
        nargs=1,
        required=True,
    )
    parser.add_argument(
        '--export-json',
        dest='json_file',
        nargs=1,
        required=True,
    )
    parser.add_argument(
        '--export-sprites-json',
        dest='sprites_file',
        nargs=1,
        type=str,
        default=[''],
    )
    parser.add_argument(
        '--include-group-images',
        dest='include_group_images',
        action='store_const',
        const=[True],
        default=[False],
        help='Whether to include the image associated with a group in the output.',
    )
    parser.add_argument('src', nargs='+')

    args = parser.parse_args(sys.argv[1:])
    xcf2atlas(
        src_paths=args.src,
        dest_image_path=args.image_file[0],
        dest_json_path=args.json_file[0],
        dest_sprites_path=args.sprites_file[0],
        max_width=args.max_width[0],
        include_group_images=args.include_group_images[0],
    )


def output_json(
    dest_img,
    all_layers,
    positions,
    dest_image_path,
    dest_json_path,
):
    # Write out the json
    json_data = {
        'meta' : {
            'format' : 'RGBA8888',
            'image' : os.path.basename(dest_image_path),
            'app' : 'xcf2atlas',
            'scale' : '1',
            'verison' : '1',
            'size' : {
                'w' : dest_img.size[0],
                'h' : dest_img.size[1],
            }
        },
        'frames' : {
            f'{layer.base_name}_{layer.name}' : {
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
    with open(dest_json_path, 'w') as file:
        json.dump(json_data, file, sort_keys=True)


def output_sprites_json(
    dest_sprites_path,
    layers,
):
    layers_by_file_name = collections.defaultdict(list)
    for layer in layers:
        layers_by_file_name[layer.base_name].append(layer)

    json_data = {}
    for file_name in sorted(layers_by_file_name):
        json_data[file_name] = {
            'name' : file_name,
            'layers' : [
                {
                    'name' : layer.name
                }
                for layer in layers
            ],
        }
    with open(dest_sprites_path, 'w') as file:
        file.write(json.dumps(json_data, sort_keys=True))


def xcf2atlas(
    src_paths,
    dest_image_path,
    dest_json_path,
    dest_sprites_path,
    max_width,
    include_group_images,
):
    for src in src_paths:
        if not os.path.exists(src):
            raise FileNotFoundError(src)

    all_layers = []
    for src in src_paths:
        all_layers += xcftools.get_layer_info(src)

    if not include_group_images:
        all_layers = [
            layer
            for layer in all_layers
            if not layer.is_group
        ]

    # Pack and save the image
    dest_img, positions = pack_images(all_layers, max_width)
    dest_img.save(dest_image_path)

    output_json(
        dest_img=dest_img,
        all_layers=all_layers,
        positions=positions,
        dest_image_path=dest_image_path,
        dest_json_path=dest_json_path,
    )

    if dest_sprites_path:
        output_sprites_json(
            dest_sprites_path=dest_sprites_path,
            layers=all_layers,
        )


if __name__ == '__main__':
    main()
