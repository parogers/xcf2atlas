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

from dataclasses import dataclass
import os
import PIL
import PIL.Image
import subprocess
import re
from gimpformats.gimpXcfDocument import GimpDocument


@dataclass
class Layer:
    name: str
    x: int
    y: int
    w: int
    h: int
    image: PIL.Image
    base_name: str
    is_group: bool


def get_layer_info(src):
    '''Returns a list of layers found in the XCF file.'''

    doc = GimpDocument(src)
    layers = []
    for layer in doc.layers:
        layer = Layer(
            name=layer.name,
            x=layer.xOffset,
            y=layer.yOffset,
            w=layer.width,
            h=layer.height,
            image=layer.image,
            base_name=os.path.splitext(os.path.basename(src))[0],
            is_group=bool(layer.isGroup),
        )
        layers.append(layer)
    return layers
