import pandas as pd

# RR interval quality constants
UNRELIABLE_RR = 0x80
NOISY_RR = 0x01  # QRS detected in signal with noise
rr_qa_constants = [UNRELIABLE_RR]

# Breathing rate quality constants
RESP_STATUS_NO_A = 0x01  # Resp channel A (thoracic) is disconnected
RESP_STATUS_NO_B = 0x02  # Resp channel B (abdominal) is disconnected
RESP_STATUS_BASELINE_A = 0x04  # Resp A baseline has changed.
RESP_STATUS_BASELINE_B = 0x08  # Resp B baseline has changed.
RESP_STATUS_NOISY_A = 0x10  # Resp A has high frequency content.
RESP_STATUS_NOISY_B = 0x20  # Resp B has high frequency content.
br_qa_constants = [RESP_STATUS_NO_A, RESP_STATUS_NO_B, RESP_STATUS_BASELINE_A,
                   RESP_STATUS_BASELINE_B]

# Heart rate quality constants
ECG_FOR_FUTURE_USE = 0x01  # reserved to reach heart ECG
ECG_STATUS_DISCONNECTED = 0x02  # Shirt is disconnected
ECG_STATUS_50_60HZ = 0x04  # 50-60 Hz dominant in ECG.
ECG_STATUS_SATURATED = 0x08  # ECG signal saturated
ECG_STATUS_ARTIFACTS = 0x10  # Movement artifacts makes RR intervals less precise
ECG_STATUS_UNRELIABLE_RR = 0x20  # ECG ok, but some RR are unreliable
hr_qa_constants = [ECG_STATUS_DISCONNECTED, ECG_STATUS_UNRELIABLE_RR]


def clean_hx_series(df, quality_df, qa_constants):
    """
    Cleans time-series by removing any rows that have a quality score with
    one or more of the qa_constant bits flipped (indicating an unreliable
    reading).

    NOTE: Assumes DataFrames with header = ["datetime", "values"]

    Args:
        df (DataFrame): Contains raw values for hexoskin feature
        quality_df (DataFrame): Contains quality scores
        qa_constants (list): List containing relevant quality score constants

    Returns:
        (DataFrame): New DataFrame only containing quality readings.

    Raises:
        ValueError: If dates don't align between df and quality_df
    """
    # Verify that dates are time aligned
    if not quality_df["datetime"].equals(df["datetime"]):
        raise ValueError("Dates are not aligned between 'df' and 'quality_df'")

    # Convert columns to ndarrays for simplicity (& increased performance?)
    raw_values = df["values"].values
    quality_scores = quality_df["values"].values
    datetimes = quality_df["datetime"].values

    # Build new data frame with only quality readings
    new_series = {
        "datetime": [],
        "values": []
    }
    for i, score in enumerate(quality_scores):
        is_reliable = True
        for const in qa_constants:
            if int(score) & int(const):
                is_reliable = False
                break

        if is_reliable:
            new_series["datetime"].append(datetimes[i])
            new_series["values"].append(raw_values[i])

    return pd.DataFrame.from_dict(new_series)
