
import os
import json


def output_json(
    dest_img,
    all_layers,
    placed_imgs,
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
            f'{placed_img.layer.base_name}_{placed_img.layer.name}' : {
                'frame' : {
                    'x' : placed_img.x,
                    'y' : placed_img.y,
                    'w' : placed_img.layer.w,
                    'h' : placed_img.layer.h
                },
                'rotated' : False,
                'trimmed' : False,
                'spriteSourceSize' : {
                    'x' : 0,
                    'y' : 0,
                    'w' : placed_img.layer.w,
                    'h' : placed_img.layer.h
                },
                'sourceSize' : {'w' : placed_img.layer.w, 'h' : placed_img.layer.h},
                'pivot' : {'x' : 0.5, 'y' : 0.5}
            }
            for placed_img in placed_imgs
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
        file.write(json.dumps(json_data, sort_keys=True, indent=4))
