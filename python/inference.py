import argparse
import pickle


def main(args):
    model = pickle.load(open(args.model, "rb"))
    test = pickle.load(open(args.test, "rb"))


    print('Done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True,
                        help="File containing saved model (a pkl)")
    parser.add_argument("--test", type=str,
                        help="File containing test data (a pkl)")

    main(parser.parse_args())