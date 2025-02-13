import argparse

def setup_parser():
    """Sets up the argument parser for the traceroute program

    :return: parser, an initialized ArgumentParser object
    :rtype: ArgumentParser
    """
    parser = argparse.ArgumentParser(description="Open Packet Capture File, "
                                                 "filter packets and Display"
                                                 " Packet Headers")
    parser.add_argument("-n", help="Print hop addresses numerically only")
    parser.add_argument("-q", help="Number of probes per TTL",
                        type=int)
    parser.add_argument("-S", help="Summary of how many probes "
                                   "unanswered for each hop")
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()