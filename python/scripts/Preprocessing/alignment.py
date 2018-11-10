import pandas as pd

def get_time_range(df_map):
    min_time, max_time = (None for i in range(2))

    # Find min and max time from each df and update overall min/max.
    for feature in df_map:
        df = df_map[feature]

        # Update min
        df_min = min(df["datetime"])
        if min_time is None or min_time > df_min:
            min_time = df_min

        # Update max
        df_max = max(df["datetime"])
        if max_time is None or max_time > df_max:
            max_time = df_max

    return min_time, max_time


def init_combined_dataframe(df_map, timedelta):
    """
    Crete a DataFrame with each row corresponding to a period of time in the
    series (as specified by 'timedelta').

    :param df_map (dict): Feature -> DataFrame mapping
    :param timedelta (obj): Timedelta object specifying
    :return:
    """
    print("Initializing combined dataframe...")

    min_time, max_time = get_time_range(df_map)

    # Create DataFrame with row for each
    columns = ["datetime"] + list(df_map.keys())

    df = pd.DataFrame(columns=columns)
    df["datetime"] = pd.date_range(min_time, max_time, freq=timedelta)

    return df


def populate_combined_dataframe(combined_df, df_map):
    print("Populating combined dataframe...")
    start_time = combined_df.iloc[0]["datetime"]

    for i in range(1, combined_df.shape[0]):
        end_time = combined_df.iloc[i]["datetime"]

        # For each feature, get the average value over values in time period
        for feature in df_map:
            df = df_map[feature]

            # Get values in [start_time, end_time]
            mask = ((df["datetime"] >= start_time) & (df["datetime"] < end_time))
            subset = df.loc[mask]

            # Place value into combined_df
            if not subset.empty:
                combined_df[feature].iat[i - 1] = subset["values"].mean()
            else:
                combined_df[feature].iat[i - 1] = -1

    return combined_df


def merge_dataframes(df_map, frequency):
    """
    Merges all feature DataFrames into one at the specified frequency

    :param df_map (dict): Feature -> DataFrame mapping.
    :param frequency (timedelta): Sampling rate as a timedelta object.
    :return (DataFrame): Merged DataFrame aligned on time.
    """
    combined_df = init_combined_dataframe(df_map, frequency)
    combined_df = populate_combined_dataframe(combined_df, df_map)

    return combined_df
