# MR CLEAN
With Mr. Clean, no dataset is safe! (Unless it's clean, or in a format other than DataFrame.)

## Plan

0. Make a copy of the inputted DataFrame
1. Diagnose problems with underlying data format
2. Handle missing values
3. Change data formats
4. Do melts and pivots (If necessary)
5. Print what was done

#### Diagnose underlying problems

These are problems that hinder every other operation that could be done, and include:

- All entries contain characters that prevent the dataframe from being read in correctly.
- Rows are labeled with names that make it harder to do analysis
- Data is corrupted
- No entries
- Entries are encoded wrong

#### Handling missing values

1. Change missing values to NaN, using some logic to do this.
2. Fill missing values, using logic and some user inputs

#### Changing data formats

1. Coerce columns to numerics and datetimes
2. Change columns to categorical
3. Handle missing values again

#### Melts and pivots

1. Infer columns that need to be melted or pivoted
2. Do it.
3. If a melt was performed, convert the 'variable' column to a categorical column

#### Print what was done

Print exactly what was done, and a (useful) summary of the dataset, after each action.



#### Params

df
settings - This should be a dictionary. If it is, then the method will use it for all settings. Any not included will be set to the default.
col_names
handle_na - function to use to handle missing rows
char_scrub  - whether or not to perform a char scrub
char_scrub_cutoff - cutoff for when to stop scrubbing, i.e. what percentage needs to have the same character in order to scrub
scrub_ignore - a list of column names to ignore when scrubbing
numeric_cutoff - Cutoff for coercing a numeric i.e. what percentage needs to be a numeric in order to allow a numeric coercion
coerce_numeric - Columns explicitly meant to be converted to numeric
dt_cutoff - Cutoff for coercing a numeric i.e. what percentage needs to be a numeric in order to allow a numeric coercion
coerce_dt - Columns explicitly meant to be converted to numeric
dt_format - Format string for date-time characters
categorical_cutoff - Cutoff for coercing a categorical i.e. what percentage of the column entries are duplicates
coerce_categorical - Columns explicitly meant to be converted to numeric
display_preview - Whether or not to display the preview
preview_rows - Rows of the head and tail to preview
preview_max_cols - Max cols to preview
output_file - Filepath to output to. If None, will return the dataframe instead.
output_safe - May overwrite an existing file if and only if output_safe is False



Separate files into:

utils
data utils
printing utils

Low level cleaning and formatting
table-blind actions
single column actions
collecting and formatting metadata
collecting data on relationships between columns

2nd level formatting
inferring best action for single column
parsing metadata

3rd level
relationships between multiple columns



4th level


meta-data parsing

actions for small subset of table
actions for 







