# args: all_participants directory
# pct in test
# bag interval
# [model params]

import trainer
import inference as tester
import gen_bags as MIL
import gen_min_to_min as min2min
import gen_flat_feature_file as flat
import argparse
import sys
import os

# python pipeline.py [path to smoking_data] 30 .1 RF --sklearn 1
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("base_dir", type=str,
                        help="Directory containing all participant data.")
    parser.add_argument("bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("pct_test", type=float,
                        help="Percent of data used for test set")
    parser.add_argument("--train", type=str,
                       help="File containing training data (a pkl)")
    parser.add_argument("model", type=str,
                        choices=["RF", "miSVM", "MISVM", "LRC", "GBC", 
                        "SVM"],
                        help="Model type")
    parser.add_argument("--hyperopt", type=int,
                        help="Number of hyperparameter iterations for "
                             "hyperopt tuning.")
    parser.add_argument("--sklearn", type=int,
                        help="Number of hyperparameter iterations for sklearn "
                             "tuning.")
    parser.add_argument("--take_mean", action='store_true', default=False,
                        help="Use the feature mean for each bag as one "
                             "instance (as opposed to stacking multiple "
                             "instances as the input to the model).")


    testParser = argparse.ArgumentParser()



    testParser.add_argument("--model", type=str, required=False,
                        help="File containing saved model (a pkl)")
    testParser.add_argument("--test", type=str,
                        help="File containing test data (a pkl)")                             

    temp_args = parser.parse_args()
    
    train_pkl_path = temp_args.base_dir+"/train_intv=%s_min.pkl"%temp_args.bag_interval
    test_pkl_path = temp_args.base_dir+"/test_intv=%s_min.pkl"%temp_args.bag_interval
    args = parser.parse_args(args=[*sys.argv[1:], "--train", train_pkl_path])

    # args = parser.parse_args(args=[*sys.argv[1:], "--train",train_pkl_path])
    print(args)

    print("Preprocessing...")
    preprocess(args)
    print("Aggregating...")
    aggregate(args)
    print("Bagging...")
    test_path = bags(args)
    print("Training...")
    model_path = train(args)
    args = testParser.parse_args(args=["--model", model_path, "--test", test_pkl_path])
    print("Testing...")
    return test(args)


    

def preprocess(args):
    participants = [filename for filename in os.listdir(args.base_dir) if filename.startswith('participant')]
    for participant in participants:
        temp_parser = argparse.ArgumentParser()
        temp_parser.add_argument("participant_dir", type=str)
        temp_args = temp_parser.parse_args(args=[args.base_dir+"/"+participant])
        flat.main(temp_args)

def aggregate(args):
    min2min.main(args)

def bags(args):
    return MIL.main(args)

def train(args):
    return trainer.main(args)
    
def test(args):
    return tester.main(args)

if __name__ == "__main__":
    main()
