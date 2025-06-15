import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commercial", action="store_true", help="Commercial build")
    parser.add_argument("--epub", action="store_true", help="EPUB. No dictionary build")
    return parser.parse_args()


ARGS = get_args()
