
import subprocess

def file_contents_match(src1, src2):
    return open(src1, 'rb').read() == open(src2, 'rb').read()

def run_xcf2atlas(args):
    return subprocess.run([
        './xcf2atlas.py',
    ] + args).returncode
