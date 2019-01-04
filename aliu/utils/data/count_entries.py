def count_entries(df, col_name):
    """Return a dictionary with counts of
    occurrences as value for each key."""

    counts = {}
    col = df[col_name]

    for entry in col:
        if entry in counts.keys():
            counts[entry]+=1
        else:
            counts[entry]=1

    return counts

import pandas as pd
def count_entries_csv(csv_file, col_name, chunksize = 10):
    """Return a dictionary with counts of
    occurrences as value for each key."""

    counts = {}

    for chunk in pd.read_csv(csv_file, chunksize = 10):
        counts.update(count_entries(chunk, col_name))

    return counts