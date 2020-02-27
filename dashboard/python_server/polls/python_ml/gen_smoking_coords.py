import argparse
from math import cos, sin, atan2, sqrt, degrees, radians
import os
import numpy as np
import pandas as pd


# Look for location up to 2**6 (i.e. 32 minutes) surrounding lapse time.
EXP_BACKOFF_CONST = 6


def center_geolocation(geolocations):
    """
    Approximates the center of a set of lat/long coordinates

    Args:
        geolocations (array-like): Set of coordinates (in degrees)

    Returns:
        (tuple): Center point coordinates (in degrees)
    """
    x, y, z = (0 for i in range(3))

    for coord in geolocations:
        lat = radians(coord[0])
        lon = radians(coord[1])
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / len(geolocations))
    y = float(y / len(geolocations))
    z = float(z / len(geolocations))

    return degrees(atan2(z, sqrt(x * x + y * y))), degrees(atan2(y, x))


def get_locations(location_df, smoking_time):
    """
    Find location data surrounding smoking episode time. Uses exponential
    back-off to increase time range.

    Args:
        location_df (obj): Dataframe containing all recorded locations
        smoking_time (datetime): Time of smoking lapse.

    Returns:
        (obj): Dataframe containing subset of data
    """
    trails = 0

    while trails < EXP_BACKOFF_CONST:
        lbound = smoking_time - np.timedelta64(2 ** trails, 'm')
        ubound = smoking_time + np.timedelta64(2 ** trails, 'm')
        mask = ((location_df["datetime"] > lbound) &
                (location_df["datetime"] < ubound))
        subset = location_df.loc[mask]

        if subset.shape[0] > 0:
            return subset

        trails += 1

    raise ValueError("Could not find valid location within %d minutes" %
                     (2 ** (trails - 1)))


def estimate_smoking_locations(smoking_df, location_df):
    # Add new columns to smoking DataFrame
    smoking_df['latitude'] = np.repeat(np.inf, smoking_df.shape[0])
    smoking_df['longitude'] = np.repeat(np.inf, smoking_df.shape[0])

    for index, row in smoking_df.iterrows():
        # Find locations at times surrounding the smoking episode.
        try:
            subset = get_locations(location_df, row["datetime"])
        except ValueError as err:
            print(err.__str__())
            continue

        coords = subset[["latitude", "longitude"]]
        row["latitude"], row["longitude"] = center_geolocation(coords.values)
        smoking_df.loc[index] = row

    return smoking_df


def main(args):
    os.chdir(args.base_dir)

    # Get each participant directory
    participants = [filename for filename in os.listdir('./') if
                    filename.startswith('participant')]

    smoking_locations = pd.DataFrame()
    for participant in participants:
        # Change to the participant's EMA directory
        os.chdir(participant+"/ema")

        # Load in location data, sort by date
        location_df = pd.read_csv("location.csv", index_col=0, header=0)
        location_df["datetime"] = pd.to_datetime(location_df["datetime"])
        location_df = location_df.sort_values("datetime")

        # Load in smoking data, sort by date
        smoking_df = pd.read_csv("smoking_reports.csv", index_col=0, header=0)
        smoking_df["datetime"] = pd.to_datetime(smoking_df["datetime"])
        smoking_df = smoking_df.sort_values("datetime")

        # Get smoking locations
        smoking_df = estimate_smoking_locations(smoking_df, location_df)

        # Add participant id
        pid = participant.split("_")[1]
        smoking_df['participant_id'] = np.repeat(pid, smoking_df.shape[0])

        smoking_locations = smoking_locations.append(smoking_df)

        os.chdir('../../')

    # Clean-up DataFrame before writing to file
    smoking_locations = smoking_locations[["participant_id", "datetime",
                                          "latitude", "longitude"]]
    smoking_locations = smoking_locations.replace(np.inf, np.nan)
    smoking_locations.to_csv('smoking_locations.csv', na_rep='NA', index=False)
    print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_dir", type=str,
                        help="Base directory for all participant data.")

    main(parser.parse_args())
