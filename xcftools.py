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

from typing import List
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
    layers: List['Layer']

    @property
    def sprite_name(self):
        return f'{self.base_name}_{self.name}'

    def __getitem__(self, index):
        return self.layers[index]


def get_layer_info(src):
    '''Returns a list of layers found in the XCF file.'''

    doc = GimpDocument(src)
    layers = []
    for gimp_layer in doc.layers:
        layer = Layer(
            name=gimp_layer.name,
            x=gimp_layer.xOffset,
            y=gimp_layer.yOffset,
            w=gimp_layer.width,
            h=gimp_layer.height,
            image=gimp_layer.image,
            base_name=os.path.splitext(os.path.basename(src))[0],
            is_group=bool(gimp_layer.isGroup),
            layers=[],
        )

        if gimp_layer.itemPath:
            slice = layers
            for path in gimp_layer.itemPath[:-1]:
                slice = slice[path].layers
            assert gimp_layer.itemPath[-1] == len(slice)
            slice.append(layer)
        else:
            layers.append(layer)

    return layers
