import numpy as np
import pandas as pd


# todo: Rewrite using NN_intervals and a sliding window approach.
def gen_hrv_by_minute(rr_df, method):
    """
    Generates dataframe containing minute-to-minute HRV.

    :param rr_df (obj): Dataframe containing RR intervals over time.
    :param method (str): Method used to compute HRV
    :return (obj): Dataframe containing minute-to-minute HRV
    """

    # Setup HRV dataframe
    hrv_df = pd.DataFrame(columns=["datetime", "hrv"])

    # Compute using Root Mean Sum of Square Differences of adjacent RR intervals
    if method == "rmssd":
        start_time = rr_df.iloc[0]["datetime"]  # Starting at first minute
        row_idx = 0

        # Compute HRV for each consecutive minute
        while start_time < rr_df.iloc[rr_df.shape[0] - 1]["datetime"]:
            end_time = start_time + np.timedelta64(1, 'm')

            # Extract subset between start and end times.
            mask = ((rr_df["datetime"] > start_time) &
                    (rr_df["datetime"] < end_time))
            subset = rr_df.loc[mask]

            # If there exists more than two valid RR's, compute RMSSD
            if subset.shape[0] > 1:
                hrv_df.loc[row_idx] = [start_time,
                                       calc_rmssd(np.asarray(subset["rr"]))]
                row_idx += 1

            start_time = start_time + np.timedelta64(1, 'm')
    hrv_df.to_csv("hrv_timestamps.csv")


def calc_sq_diffs(rr_intervals):
    """
    Computes square differences over array.

    :param rr_intervals (ndarray): RR intervals over time (length=N).
    :return (list): Square differences (length = N-1)
    """
    sq_diffs = []

    prev = rr_intervals[0]
    for rr in rr_intervals[1:]:
        sq_diffs.append(np.square(rr - prev))
        prev = rr

    return sq_diffs


def calc_rmssd(rr_intervals):
    """
    Computes Root Mean Sum of Square Differences (RMSSD) of adjacent RR
    intervals

    :param rr_intervals (ndarray): RR intervals over time
    :return (float): RMSSD over provided list.
    """
    sq_diffs = calc_sq_diffs(rr_intervals)
    return np.sqrt(np.mean(sq_diffs))