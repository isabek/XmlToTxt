import argparse
import os

import sys

from transformer import Transformer


def main():
    parser = argparse.ArgumentParser(description="Formatter from ImageNet xml to Darknet text format")
    parser.add_argument("-xml", help="Relative location of xml files directory", required=True)
    parser.add_argument("-out", help="Relative location of output txt files directory", default="out")
    args = parser.parse_args()

    xml_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), args.xml)
    if not os.path.exists(xml_dir):
        print("Provide the correct folder for xml files.")
        sys.exit()

    out_dir = os.path.join(os.path.dirname(os.path.realpath('__file__')), args.out)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not os.access(out_dir, os.W_OK):
        print("%s folder is not writeable.")
        sys.exit()

    transformer = Transformer(xml_dir=xml_dir, out_dir=out_dir)
    transformer.transform()


if __name__ == "__main__":
    main()
