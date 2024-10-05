# xcf2atlas

Converts a set of XCF files into an image atlas suitable for loading with eg. pixi.js or other libraries. The layers of each XCF are separated out and packed into a larger (final) image. This program also generates an accompanying JSON file that gives the location and size of each image in the atlas, along with an associated name.

The name of each sprite in the atlas is:

    <FILE NAME>_<LAYER NAME>

Where <FILE NAME> is the name of the file, minus the extension.

## Dependencies

You'll need the python [gimpformats](https://pypi.org/project/gimpformats/) module installed.

## Usage

xcf2atlas.py --export-image output.png --export-json output.json input.xcf
