
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
