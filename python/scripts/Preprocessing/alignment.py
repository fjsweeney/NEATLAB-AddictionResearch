import pandas as pd


def get_time_range(df_map):
    """
    Gets the overall min and max time from all sensor DataFrames

    :param df_map (dict): Feature -> DataFrame mapping
    :return (tuple): Min and max times, respectively.
    """
    min_time, max_time = (None for i in range(2))

    # Find min and max time from each df and update overall min/max.
    for feature in df_map:
        df = df_map[feature]
        try:
            # Update min
            df_min = min(df["datetime"])
            if min_time is None or min_time > df_min:
                min_time = df_min

            # Update max
            df_max = max(df["datetime"])
            if max_time is None or max_time > df_max:
                max_time = df_max
        except ValueError as err:
            print("%s for feature: %s" % (err.__str__(), feature))

    return min_time, max_time


def init_combined_dataframe(df_map, timedelta):
    """
    Crete a DataFrame with each row corresponding to a period of time in the
    series (as specified by 'timedelta').

    :param df_map (dict): Feature -> DataFrame mapping
    :param timedelta (obj): Timedelta object specifying
    :return (DataFrame): Initialized DataFrame
    """
    print("Initializing combined dataframe...")

    min_time, max_time = get_time_range(df_map)

    # Create DataFrame with row for each
    columns = ["datetime"] + list(df_map.keys())

    df = pd.DataFrame(columns=columns)
    df["datetime"] = pd.date_range(min_time, max_time, freq=timedelta)

    return df


def populate_combined_dataframe(combined_df, df_map):
    """
    Populate combined Dataframe with Hexoskin and Android data

    :param combined_df (DataFrame): Initialized DataFrame
    :param df_map (dict): Feature -> DataFrame mapping
    :return (DataFrame): Populated DataFrame
    """
    print("Populating combined dataframe...")
    start_time = combined_df.iloc[0]["datetime"]

    feature_idxs = {key: 0 for key in list(df_map.keys())}

    for i in range(1, combined_df.shape[0]):
        # Update progress bar every once in awhile...
        if (i % (combined_df.shape[0]//100)) == 0:
            print("%d%% complete..." % ((i/combined_df.shape[0])*100))

        end_time = combined_df.iloc[i]["datetime"]

        # For each feature, get the average value over values in time period
        for feature in df_map:
            df = df_map[feature]

            # If multiple values in time range, compute the mean.
            row_sum, row_cnt = (0.0 for i in range(2))
            curr_idx = feature_idxs[feature]
            try:
                while not df.empty and \
                        start_time <= df.iloc[curr_idx]["datetime"] < end_time:
                    row_sum += df.iloc[curr_idx]["values"]
                    row_cnt += 1
                    curr_idx += 1
            except IndexError as err:
                print("%s for feature %s at index %d" %
                      (err.__str__(), feature, curr_idx))


            # Update feature index
            feature_idxs[feature] = curr_idx

            # Place value into combined_df
            if row_cnt == 0:
                combined_df[feature].iat[i-1] = -1
            else:
                combined_df[feature].iat[i-1] = row_sum/row_cnt

        # Shift time window
        start_time = end_time

    return combined_df


def remove_empty_rows(df):
    """
    Removes empty rows from DataFrame (i.e. where data == -1.0)

    :param df (DataFrame): A DataFrame
    :return (DataFrame): DataFrame with empty rows removed
    """
    # Get all column names except for the datetime column.
    columns = list(df)
    columns.remove("datetime")

    # Create filter to include all "empty" rows
    mask = (df[columns[0]] == -1.0)
    for column in columns[1:]:
        mask = mask & (df[column] == -1.0)

    # Return all "non-empty" rows by negating the mask.
    return df.loc[~mask]


def merge_dataframes(df_map, frequency, remove_empties=True):
    """
    Merges all feature DataFrames into one at the specified frequency

    :param df_map (dict): Feature -> DataFrame mapping.
    :param frequency (timedelta): Sampling rate as a timedelta object.
    :param remove_empties (bool): Remove empty rows from DataFrame
    :return (DataFrame): Merged DataFrame aligned on time.
    """
    combined_df = init_combined_dataframe(df_map, frequency)
    combined_df = populate_combined_dataframe(combined_df, df_map)

    if remove_empties:
        return remove_empty_rows(combined_df)

    return combined_df
