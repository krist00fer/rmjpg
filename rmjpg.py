#!/usr/bin/env python3

import argparse
import os
import glob

parser = argparse.ArgumentParser(description="Remove JPG-files if RAW file exists.")
parser.add_argument('--path', nargs='?', default='.', help='path to look into, defaults to current.')
parser.add_argument('--move-to', nargs='?', default='.', help='path to move jpgs to if RAW file is found.')
args = parser.parse_args()


jpg_extensions = ['jpg', 'jpeg']
raw_extensions = ['cr2', 'dng']

jpg_extensions.extend([x.upper() for x in jpg_extensions])
raw_extensions.extend([x.upper() for x in raw_extensions])

for jpg_extension in jpg_extensions:
    files = glob.glob(os.path.join(args.path, '*.' + jpg_extension))

    for full_file_name in files:
        (file_name, file_extension) = os.path.splitext(full_file_name)

        has_raw_file = False

        for raw_extension in raw_extensions:
            raw_file = file_name + '.' + raw_extension
            if os.path.exists(raw_file):
                has_raw_file = True
                break

        if has_raw_file and args.move_to:
                new_file_name = os.path.join(args.move_to, os.path.basename(full_file_name))
                print('Moving ' + full_file_name + ' to ' + new_file_name)
                os.replace(full_file_name, new_file_name)

