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

def get_layer_info(src):
    """Returns a list of layers found in the XCF file."""

    Layer = namedtuple("layer", ("name", "x", "y", "w", "h"))

    proc = subprocess.Popen(["xcfinfo", src], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    layers = []
    for line in out.decode("UTF-8").split("\n"):
        m = re.match("^\+ (\d+)x(\d+)\+(\d+)\+(\d+) [^ ]* [^ ]* (.+)$", line)
        if (m):
            (w, h, x, y, name) = m.groups()
            layers.append(Layer(name, int(x), int(y), int(w), int(h)))
    return layers

#def extract_layer_to_png(src, dest, layer_name):
#    proc = subprocess.Popen(["xcf2png", src, layer_name, "-o", dest])
#    proc.wait()

def extract_layer(src, layer_name):
    proc = subprocess.Popen(
        ["xcf2png", src, layer_name], 
        stdout=subprocess.PIPE
    )
    out, err = proc.communicate()
    return PIL.Image.open(io.BytesIO(out))
