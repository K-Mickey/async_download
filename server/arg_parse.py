import argparse

import config


def run_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logging', action='store_true', help='Enable access log')
    parser.add_argument('-d', '--enable-delay', action='store_true', help='Enable server response delay')
    parser.add_argument('-f', '--photo-dir', default=config.PHOTO_DIR, action='store', help='Photo direction')

    namespace = parser.parse_args()
    config.LOGGING = namespace.logging
    config.ENABLE_DELAY = namespace.enable_delay
    config.PHOTO_FOLDER = namespace.photo_dir
