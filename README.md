# xcf2atlas

Converts a set of XCF files into a large image atlas. The layers of each XCF
are separated out and packed into a larger (final) image. This program also
generates an accompanying JSON file that gives the location and size of each
image in the atlas, along with an associated name.

## Dependencies

You'll need the python [gimpformats](https://pypi.org/project/gimpformats/) module installed.

## Usage

xcf2atlas.py --export-image output.png --export-json output.json input.xcf
