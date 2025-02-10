import argparse

def setup_parser():
    """Sets up the argument parser for the traceroute program

    :return: parser, an initialized ArgumentParser object
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("-n", help="Number of hop addresses to hop",
                        type=int)
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()