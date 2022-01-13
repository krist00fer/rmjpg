#!/usr/bin/env python3

import argparse
import os

parser = argparse.ArgumentParser(
    description="Remove JPG-files if RAW file exists.")
parser.add_argument('--path', nargs='?', default='.',
                    help='path to look into, defaults to current.')
parser.add_argument('--trash', nargs='?', default='trash',
                    help='path to move found JPGs to (i.e files are not removed)')
parser.add_argument('--remove', nargs='?', default=False,
                    help='set to True to execute, otherwise will only simulate removal')
args = parser.parse_args()


def remove_file(file):
    if (args.remove):
        print(f'Moving {file} to {args.trash}')
        os.replace(file, os.path.join(args.trash, os.path.basename(file)))
    else:
        print(f'{file} would be (re)moved')


jpg_extensions = ['.JPG', '.JPEG']
raw_extensions = ['.RWZ', '.RAF', '.CR2', '.RW2', '.ERF', '.NRW', '.DNG', '.NEF',
                  '.K25', '.ARW', '.SRF', '.EIP', '.DNG', '.DCR', '.RAW', '.CRW',
                  '.3FR', '.BAY', '.CS1', '.MEF', '.KDC', '.ORF', '.SR2', '.ARI',
                  '.MOS', '.FFF', '.MFW', '.CR3', '.SRW', '.J6I', '.RWL', '.X3F',
                  '.KC2', '.MRW', '.PEF', '.IIQ', '.CXI', '.NKSC', '.MDC']

# Files need to be taken/modified within these number of seconds to be considered as taken at the same time
max_modified_time_diff = 10

with os.scandir(args.path) as dir_entries:
    files = sorted(list(dir_entries), key=lambda x: x.path)

    last_file_name = ''
    last_file_extension = ''
    last_was_jpg = False
    last_st_mtime = 0
    jpg_in_set_removed = False

    for file in files:
        info = file.stat()
        (file_name, file_extension) = os.path.splitext(file.path)
        st_mtime = info.st_mtime
        is_jpg = file_extension.upper() in jpg_extensions
        is_raw = file_extension.upper() in raw_extensions

        if is_jpg or is_raw:
            if file_name == last_file_name:
                # We are exploring a set of files that are similarly named
                if abs(info.st_mtime - last_st_mtime) < max_modified_time_diff:
                    # The two files are created/modified around the same time
                    if is_jpg:
                        remove_file(f'{file_name}{file_extension}')
                        jpg_in_set_removed = True
                    elif last_was_jpg and not jpg_in_set_removed:
                        remove_file(f'{last_file_name}{last_file_extension}')
                        jpg_in_set_removed = True
            else:
                # Since filename wasn't the same as last, we are in a new set of files... possibly
                jpg_in_set_removed = False

        last_file_name = file_name
        last_file_extension = file_extension
        last_was_jpg = is_jpg
        last_st_mtime = st_mtime
