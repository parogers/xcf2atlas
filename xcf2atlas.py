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
import json
import sys
import os
import argparse

import xcftools
from output import (
    output_json,
    output_sprites_json,
)
from packing import (
    pack_images,
)


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

    # Pack and save the image
    dest_img, placed_imgs = pack_images(
        all_layers,
        max_width,
        include_group_images=include_group_images,
    )
    dest_img.save(dest_image_path)

    output_json(
        dest_img=dest_img,
        all_layers=all_layers,
        placed_imgs=placed_imgs,
        dest_image_path=dest_image_path,
        dest_json_path=dest_json_path,
    )

    if dest_sprites_path:
        output_sprites_json(
            dest_sprites_path=dest_sprites_path,
            layers=all_layers,
        )


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


if __name__ == '__main__':
    main()
