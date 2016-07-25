#!/usr/bin/env python

from __future__ import print_function

from argparse import ArgumentParser
import sys

from lxml.html import html5parser


def split_class_list(class_list):
    """
    Split a space-separated list of classes into a list of class names

    Any template expressions contained in curly braces in `class_list`
    are skipped over.
    """

    brace_depth = 0
    classes = []
    cls = ''

    for ch in class_list + ' ':
        if ch == '{':
            brace_depth += 1
        elif ch == '}':
            brace_depth -= 1
        elif brace_depth == 0:
            if ch.isspace():
                cls = cls.strip()
                if cls:
                    classes.append(cls)
                    cls = ''
            else:
                cls += ch

    return classes


def used_html_classes(path):
    """
    Return a list of CSS classes which are referenced by "class" attributes on
    tags in an HTML file or template for an HTML file.
    """

    root = html5parser.parse(path)
    classes = set()
    for e in root.findall('//*[@class]'):
        class_attr = e.get('class')
        if class_attr is None:
            continue
        class_list = split_class_list(class_attr)
        for cls in class_list:
            classes.add(cls)
    return classes


def main():
    parser = ArgumentParser()
    parser.add_argument('files', metavar='files', nargs='+', help="List of HTML files or templates to parse")
    args = parser.parse_args()

    classes = set()

    for path in args.files:
        classes.update(used_html_classes(path))

    for cls in sorted(classes):
        print(cls)


if __name__ == '__main__':
    main()
