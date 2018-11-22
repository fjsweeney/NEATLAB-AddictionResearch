import argparse
import os


def main(args):
    # Change to participant's hexoskin directory
    os.chdir(args.participant_dir)

    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Change to findings location")

    main(parser.parse_args())
