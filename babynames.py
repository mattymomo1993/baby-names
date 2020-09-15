#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

__author__ = """Matthew, Mike Boring, Kyle Hastings"""
"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    sorting_names = []
    with open(filename) as f:
        text = f.read()
        year = r'Popularity\sin\s(\d\d\d\d)'
        y = re.search(year, text)
        sorting_names.append(
            text[y.start():y.end()].replace('Popularity in ', ''))
        for text_section in text.split():
            if text_section.startswith('align="right"><td>'):
                sorting_names.append(text_section.replace(
                    'align="right"><td>', '').replace(
                    '</td><td>', ' ').replace('</td>', ''))
    final_list = []
    for single_name in sorting_names:
        if single_name == sorting_names[0]:
            final_list.append(single_name)
        else:
            split_single_name = single_name.split()
            if len(split_single_name) == 3:
                if split_single_name[1]+' ' not in ' '.join(final_list):
                    final_list.append(
                        split_single_name[1] + ' ' + split_single_name[0])
                if split_single_name[2]+' ' not in ' '.join(final_list):
                    final_list.append(
                        split_single_name[2] + ' ' + split_single_name[0])
                continue
    final_sorted_list = sorted(final_list)
    return final_sorted_list


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)
    if not ns:
        parser.print_usage()
        sys.exit(1)
    file_list = ns.files
    # option flag
    create_summary = ns.summaryfile
    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).

    if create_summary:
        for name_list in file_list:
            with open(name_list + '.summary', 'w') as f:
                new_list = extract_names(name_list)
                for name in new_list:
                    f.write(name + '\n')
    else:
        for name_list in file_list:
            new_list = extract_names(name_list)
            for name in new_list:
                print(name)


if __name__ == '__main__':
    main(sys.argv[1:])
