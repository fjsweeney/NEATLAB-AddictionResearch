import argparse
import json
import pytz
import os
from datetime import datetime
import pandas as pd

# For converting datetimes to PST (NOTE: WE ASSUME PST IN THIS SCRIPT)
pst = pytz.timezone('US/Pacific')
fmt = '%Y-%m-%d %H:%M:%S'


def export_ema(ema_responses):
    responses = []

    for response in ema_responses[1:]:
        clean_response = {}

        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(float(response['timeUTC'])/1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))
        clean_response["time"] = pst_datetime.strftime(fmt)
        clean_response["responses"] = {}

        # Empty EMA responses do not contain this attribute.
        if 'usersAllEMAAnswers' in response:
            for question in response['usersAllEMAAnswers']:
                question_obj = response['usersAllEMAAnswers'][question]
                clean_response["responses"][question_obj['question']] = \
                    question_obj['answer']

        responses.append(clean_response)

    json.dump(responses, open("ema_responses.json", 'w'))


def export_location(location_records):
    location_df = pd.DataFrame(columns=["datetime", "accuracy", "altitude",
                                        "latitude", "longitude", "provider"])

    for i, record in enumerate(location_records.values()):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(
            float(record['timeUTC']) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        location_df.loc[i] = [pst_datetime.strftime(fmt),
                          record["accuracy"],
                          record["altitude"],
                          record["latitude"],
                          record["longitude"],
                          record["provider"]]

    location_df.to_csv("location.csv", sep=",")


def export_smoking_reports(smoking_records):
    smoking_df = pd.DataFrame(columns=["datetime"])

    for i, record in enumerate(smoking_records.values()):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(
            float(record['timeUTC']) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        smoking_df.loc[i] = [pst_datetime.strftime(fmt)]

    # Sort by date
    smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])
    smoking_df = smoking_df.sort_values("datetime")

    smoking_df.to_csv("smoking_reports.csv", sep=",")


def export_stress_reports(smoking_records):
    stress_df = pd.DataFrame(columns=["datetime", "stress"])

    for i, record in enumerate(smoking_records.values()):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(
            float(record['timeUTC']) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        stress_df.loc[i] = [pst_datetime.strftime(fmt),
                            record["stressValue"]]

    # Sort by date
    stress_df["datetime"] = pd.to_datetime(stress_df["datetime"])
    stress_df = stress_df.sort_values("datetime")

    stress_df.to_csv("stress_reports.csv", sep=",")


def export_urge_reports(urge_records):
    urge_df = pd.DataFrame(columns=["datetime", "urge"])

    for i, record in enumerate(urge_records.values()):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(
            float(record['timeUTC']) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        urge_df.loc[i] = [pst_datetime.strftime(fmt),
                            record["urgeValue"]]

    # Sort by date
    urge_df["datetime"] = pd.to_datetime(urge_df["datetime"])
    urge_df = urge_df.sort_values("datetime")

    urge_df.to_csv("urge_reports.csv", sep=",")


def export_light_data(light_records):
    light_df = pd.DataFrame(columns=["datetime", "lux"])

    for i, time_utc in enumerate(light_records):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(float(time_utc) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        light_df.loc[i] = [pst_datetime.strftime(fmt), light_records[time_utc]]

    # Sort by date
    light_df["datetime"] = pd.to_datetime(light_df["datetime"])
    light_df = light_df.sort_values("datetime")

    light_df.to_csv("light_data.csv", sep=",")


def export_noise_data(noise_records):
    noise_df = pd.DataFrame(columns=["datetime", "amplitude"])

    for i, time_utc in enumerate(noise_records):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(float(time_utc) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        noise_df.loc[i] = [pst_datetime.strftime(fmt), noise_records[time_utc]]

    # Sort by date
    noise_df["datetime"] = pd.to_datetime(noise_df["datetime"])
    noise_df = noise_df.sort_values("datetime")

    noise_df.to_csv("noise_data.csv", sep=",")


def export_step_data(step_records):
    step_df = pd.DataFrame(columns=["datetime", "step_count"])

    for i, time_utc in enumerate(step_records):
        # Convert UTC to PST
        utc_datetime = datetime.utcfromtimestamp(float(time_utc) / 1000)
        utc_datetime = utc_datetime.replace(tzinfo=pytz.utc)
        pst_datetime = utc_datetime.astimezone(pytz.timezone('US/Pacific'))

        step_df.loc[i] = [pst_datetime.strftime(fmt), step_records[time_utc]]

    # Sort by date
    step_df["datetime"] = pd.to_datetime(step_df["datetime"])
    step_df = step_df.sort_values("datetime")

    step_df.to_csv("step_data.csv", sep=",")


def main(args):
    os.chdir(args.base_dir)
    file = json.loads(open(args.json, 'r').read())

    print("Exporting EMA data...", end=" ")
    export_ema(file['ema'])
    print("done")

    print("Exporting location data...", end=" ")
    export_location(file['location'])
    print("done")

    print("Exporting smoking episode data...", end=" ")
    export_smoking_reports(file['self_reported_smoking_episode'])
    print("done")

    print("Exporting stress reports...", end=" ")
    export_stress_reports(file['self_reported_stress'])
    print("done")

    print("Exporting urge reports...", end=" ")
    export_urge_reports(file['self_reported_urge'])
    print("done")

    print("Exporting ambient light data...", end=" ")
    export_light_data(file['sensors']['light'])
    print("done")

    print("Exporting noise data...", end=" ")
    export_noise_data(file['sensors']['noise'])
    print("done")

    print("Exporting step data...", end=" ")
    export_step_data(file['sensors']['step_count'])
    print("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Base directory for EMA data.")
    parser.add_argument("json", type=str,
                        help="Google firebase JSON file.")

    main(parser.parse_args())
