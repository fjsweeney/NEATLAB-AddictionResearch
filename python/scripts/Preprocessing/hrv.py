import numpy as np


def gen_hrv_by_window(df, delta, method, epsilon):
    """
    Generate HRV values over a caller-specified timedelta taking a sliding
    window approach.

    Args:
        df (DataFrame): DataFrame containing RR interval time-series.
        delta (timedelta64): Numpy timedelta specifying the time window.

    Returns:

    """
    # Create hrv column
    df["hrv"] = np.repeat(-1.0, df.shape[0])

    # Compute threshold for hrv values
    threshold = delta.item().total_seconds()*epsilon

    # Compute using Root Mean Sum of Square Differences of adjacent RR intervals
    if method == "rmssd":

        # Iterate over all possible end times
        for end_idx, row in df.iterrows():
            end_time = row["datetime"]
            start_time = end_time - delta

            # Extract subset between start and end times.
            mask = ((df["datetime"] > start_time) &
                    (df["datetime"] <= end_time) &
                    (df["RR_interval"] != -1))

            subset = df.loc[mask]

            # Compute HRV values over window if we have enough
            if subset.shape[0] >= threshold:
                df["hrv"].iat[end_idx] = \
                    calc_rmssd(subset["RR_interval"].values)

    return df


def calc_sq_diffs(rr_intervals):
    """
    Computes square differences over array.

    Args:
        rr_intervals (ndarray): RR intervals over time (length=N).

    Returns:
        (list): Square differences (length = N-1)
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
    intervals.

    Args:
        rr_intervals (ndarray): RR intervals over time

    Returns:
        (float): RMSSD over provided list.
    """
    sq_diffs = calc_sq_diffs(rr_intervals)
    return np.sqrt(np.mean(sq_diffs))