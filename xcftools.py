# xcftools.py
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

import PIL
import PIL.Image
import io
import subprocess
from collections import namedtuple
import re
from gimpformats.gimpXcfDocument import GimpDocument


def get_layer_info(src):
    '''Returns a list of layers found in the XCF file.'''

    Layer = namedtuple('Layer', ('name', 'x', 'y', 'w', 'h'))

    doc = GimpDocument(src)
    layers = []
    for layer in doc.layers:
        layer = Layer(
            name=layer.name,
            x=layer.xOffset,
            y=layer.yOffset,
            w=layer.width,
            h=layer.height,
        )
        layers.append(layer)
    return layers


def extract_layer(src, layer_name):
    doc = GimpDocument(src)
    for layer in doc.layers:
        if layer.name == layer_name:
            return layer.image
    raise ValueError(f'cannot find layer: {layer_name}')
