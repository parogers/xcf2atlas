
import os
import json
import tempfile
import pytest
from utils import (
    run_xcf2atlas,
    file_contents_match,
)


DATA_PATH = os.path.join('tests', 'data')
SAMPLE_PATH = os.path.join(DATA_PATH, 'sample-with-groups.xcf')


def test_it_exports_group_images():
    check_img_path = os.path.join(DATA_PATH, 'sample-export-with-group-images', 'out.png')
    check_json_path = os.path.join(DATA_PATH, 'sample-export-with-group-images', 'out.json')

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            '--include-group-images',
            SAMPLE_PATH,
        ])

        assert ret == 0
        file_contents_match(img_path, check_img_path)
        file_contents_match(json_path, check_json_path)


def test_it_skips_group_images():
    check_img_path = os.path.join(DATA_PATH, 'sample-export-without-group-images', 'out.png')
    check_json_path = os.path.join(DATA_PATH, 'sample-export-without-group-images', 'out.json')

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            SAMPLE_PATH,
        ])

        assert ret == 0
        file_contents_match(img_path, check_img_path)
        file_contents_match(json_path, check_json_path)


def test_it_exports_sprites_in_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        sprites_path = os.path.join(tmpdir, 'sprites.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            '--export-sprites-json', sprites_path,
            SAMPLE_PATH,
        ])

        assert ret == 0
        assert os.path.exists(sprites_path)
        sprites_data = json.loads(open(sprites_path).read())
        assert sprites_data
        assert list(sprites_data.keys()) == ['sample-with-groups']
        assert sprites_data['sample-with-groups']['name'] == 'sample-with-groups'
        # assert sprites_data['sample-with-groups']['layers'] == 'sample-with-groups'
