
import os
import json
import tempfile
import pytest

from utils import (
    run_xcf2atlas,
    file_contents_match,
)

DATA_PATH = os.path.join('tests', 'data')
SAMPLE_PATH = os.path.join(DATA_PATH, 'sample-with-nested-groups.xcf')


def test_it_exports_nested_layers():
    check_img_path = os.path.join(DATA_PATH, 'sample-export-with-nested-group-images', 'out.png')
    check_json_path = os.path.join(DATA_PATH, 'sample-export-with-nested-group-images', 'out.json')

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            SAMPLE_PATH,
        ])

        assert ret == 0
        assert file_contents_match(img_path, check_img_path)
        assert file_contents_match(json_path, check_json_path)


def test_it_exports_scene_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        scene_path = os.path.join(tmpdir, 'scene.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            '--export-scene-json', scene_path,
            SAMPLE_PATH,
        ])

        assert ret == 0
        scene_data = json.load(open(scene_path))
        assert scene_data
        assert 'sample-with-nested-groups' in scene_data
        assert scene_data['sample-with-nested-groups']['name'] == 'sample-with-nested-groups'
        assert len(scene_data['sample-with-nested-groups']['layers']) == 3
        assert scene_data['sample-with-nested-groups']['layers'][0]['name'] == 'A'
        assert scene_data['sample-with-nested-groups']['layers'][0]['sprite_name'] == 'sample-with-nested-groups_A'
        assert scene_data['sample-with-nested-groups']['layers'][1]['name'] == 'G1'
        assert len(scene_data['sample-with-nested-groups']['layers'][1]['layers']) == 2
        assert 'sprite_name' not in scene_data['sample-with-nested-groups']['layers'][1]
        assert scene_data['sample-with-nested-groups']['layers'][1]['layers'][1]['layers'][0]['name'] == 'C'
        assert scene_data['sample-with-nested-groups']['layers'][1]['layers'][1]['layers'][0]['sprite_name'] == 'sample-with-nested-groups_C'
