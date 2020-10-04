#!/usr/bin/env python3
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

import json
import tempfile
import subprocess
import os

from utils import (
    run_xcf2atlas,
    file_contents_match,
)

DATA_PATH = os.path.join('tests', 'data')
SAMPLE_PATH = os.path.join(DATA_PATH, 'sample-with-neg-pos.xcf')

def test_it_exports_all_layers():
    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            SAMPLE_PATH,
        ])

        assert ret == 0

        assert os.path.exists(img_path)
        assert os.path.exists(json_path)

        data = json.load(open(json_path))
        assert len(data['frames']) == 2

def test_it_exports_matching_png_and_json_files():
    check_img_path = os.path.join(DATA_PATH, 'sample-with-neg-pos-export-with-defaults', 'out.png')
    check_json_path = os.path.join(DATA_PATH, 'sample-with-neg-pos-export-with-defaults', 'out.json')

    with tempfile.TemporaryDirectory() as tmpdir:
        img_path = os.path.join(tmpdir, 'out.png')
        json_path = os.path.join(tmpdir, 'out.json')
        ret = run_xcf2atlas([
            '--export-image', img_path,
            '--export-json', json_path,
            SAMPLE_PATH,
        ])

        assert ret == 0

        assert os.path.exists(img_path)
        assert os.path.exists(json_path)

        assert file_contents_match(img_path, check_img_path)
        assert file_contents_match(json_path, check_json_path)
