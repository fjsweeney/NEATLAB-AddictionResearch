import argparse
import json
from decouple import config

from firebase.firebase import FirebaseApplication, FirebaseAuthentication


def init_auth():
    SECRET = config('FIREBASE_SECRET')
    EMAIL = config('FIREBASE_EMAIL')
    return FirebaseAuthentication(SECRET, EMAIL, True, True)


def main(args):
    fb = FirebaseApplication('https://smokingema-3ff13.firebaseio.com/',
                             init_auth())

    user_data = fb.get('users_data/%s' % args.user_id, None,
                       params={'print': 'pretty'},
                       headers={'X_FANCY_HEADER': 'very fancy'})

    json.dump(user_data, open(args.output, 'w'))
    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", type=str,
                        help="User ID hash")
    parser.add_argument("--output", type=str,
                        help="Path for output file.")

    main(parser.parse_args())