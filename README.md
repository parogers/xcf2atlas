# xcf2atlas

Converts a set of XCF files into an image atlas suitable for loading with eg. pixi.js or other libraries. The layers of each XCF are separated out and packed into a larger (final) image. This program also generates an accompanying JSON file that gives the location and size of each image in the atlas, along with an associated name.

The name of each sprite in the atlas is:

    <FILE NAME>_<LAYER NAME>

Where <FILE NAME> is the name of the file, minus the extension.

## Dependencies

You'll need the python [gimpformats](https://pypi.org/project/gimpformats/) module installed.

## Usage

If you just want an image atlas:

```
xcf2atlas.py --export-image output.png --export-json output.json input.xcf
```

If you want a JSON file describing the layout of the layers within the XCF you
can provide the optional '--export-scene-json' argument:

```
xcf2atlas.py --export-image output.png --export-json output.json sample-file.xcf --output-scene-json scene.json
```

Sample output:

```
{
    "sample-file": {
        "name": "sample-file",
        "layers": [
            {
                "name": "background-trees",
                "sprite_name": "sample-file_background-trees",
                "x": 0,
                "y": 0
            },
            {
                "name": "house",
                "sprite_name": "sample-file_house",
                "x": 16,
                "y": 5
            },
            {
                "name": "foreground-trees",
                "sprite_name": "sample-file_foreground-trees",
                "x": 0,
                "y": 0
            }
        ]
    }
}
```

The script will also output groups as nested layers. This is useful if your
file represents a layered scene with objects inside the layers:

```
{
    "sample-file": {
        "name": "sample-file"
        "layers": [
            {
                "name": "forest",
                "sprite_name": "sample-file_forest",
                "x": 0,
                "y": 0
            },
            {
                "name": "objects",
                "layers": [
                    {
                        "name": "house",
                        "sprite_name": "sample-file_house",
                        "x": 16,
                        "y": 0
                    },
                    {
                        "name": "boulder",
                        "sprite_name": "sample-file_boulder",
                        "x": 16,
                        "y": 0
                    }
                ]
            }
        ]
    }
}
```
