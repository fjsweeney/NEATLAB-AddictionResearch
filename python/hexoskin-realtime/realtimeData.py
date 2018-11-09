import hexoskin.client
import time
import sys
import constants
import csv
from collections import defaultdict
from hexoskin.errors import HttpBadRequest


username = "webert3@wwu.edu"
password = "smoking_cessation_2018"
publicKey = "cBciwXcJXfYc5Dl5cQ2rbwFumYcmQL"
privateKey = "7d618tMrvsQH2NW8hZPrl2r6OTHKmk"

# heart rate
HR = 19


def main(arg):



    if len(arg) < 2:
        print("MUST SPECIFY DELAY (SECONDS)")
        exit(1)

    delay = int(arg[1])

    api = hexoskin.client.HexoApi(publicKey, privateKey)
    api.auth = username+":"+password
    api.oauth2_get_access_token(username, password, scope="readonly")

    record_id = "162641"

    # switch out these lines to grab real time data
    # curr_time = time.time()
    curr_time = 394379237736/256

    start_time = int(curr_time)
    end_time = start_time + delay

    start_time *= 256
    end_time *= 256
    data_types = [constants.heartrate, constants.breathingrate, constants.rrinterval]
    output_dict = defaultdict(str)
    user_id = str(api.record.list(id=record_id)[0].user.id)
    with open("output_" + str(record_id) + ".csv", 'w') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        while True:
            try:
                data_obj = api.data.list(datatype__in=data_types, record=record_id, flat=False, no_timestamps=False,
                                         start=start_time, end=end_time)
                start_time += (delay * 256)
                end_time += (delay * 256)
                data = data_obj.__dict__['fields'][user_id]
                print(data)
                # loops through data_types and associated data
                for data_type, data_values in data.items():
                    # loops through individual pieces of data
                    for time_value in data_values:
                        time_stamp = time_value[0]
                        data_value = time_value[1]
                        print([time_stamp, data_type, data_value])
                        csv_writer.writerow([time_stamp, data_type, data_value])
            except HttpBadRequest:
                print("NO DATA AVAILABLE")

            time.sleep(delay)


if __name__ == "__main__":
    main(sys.argv)
