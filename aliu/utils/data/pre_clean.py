# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import io
import shutil
# Pre-cleaning

# This method takes in a DataFrame object, as well as a few parameters,
# and outputs a DataFrame that summarizes some of the possible problems
# that might have to be addressed in cleaning
def summary(df,preview_rows = 5,preview_max_cols = 0,
            memory_usage = 'deep',display_width = None,
            output_file = None, output_safe = True):
    """ Prints information about the DataFrame to a file or to the prompt.

    Parameters
    ----------
    df : DataFrame
        The DataFrame to summarize
    preview_rows : int, default 5
        Amount of rows to preview from the head and tail of the DataFrame
    preview_max_cols : int, default 0
        Maximum amount of columns to preview. Set to None to preview all
        columns, and set to 0 to preview as many as fit in the screen's width
    memory_usage : boolean or 'deep', default 'deep'
        Type of output that the 'memory usage' section of the .info() call should have
    display_width : int, default None
        Width of output. Can be width of file or width of console for printing.
        Set to None for pandas to detect it from console.
    output_file : path-like, default None
        If not None, this will be used as the path of the output file, and this
        function will print to a file instead of to the prompt
    output_safe : boolean, default True
        If True and output_file is not None, this function will not overwrite any
        existing files.
    """
    assert type(df) is pd.DataFrame

    # --------Values of data-----------
    df_preview = preview(df,preview_rows = 5,preview_max_cols = 0)
    info = get_info(df,verbose = True, max_cols = None,memory_usage = memory_usage,null_counts = True)
    percent_values = percentiles(df)
    # TODO add 'potential outliers' output

    # ----------Build lists------------
    title_list = ['Preview','Describe','Info']
    info_list = [df_preview,df.describe().transpose(),info]
    if percent_values is not None:
        title_list.append('Percentile Details')
        info_list.append(percent_values)
    title_list+=['Missing Values Summary','Potential Outliers']
    info_list+=[data_types(df),None]
    output = list(zip(title_list,info_list))

    # -------Print or output-----------

    # Get initial display settings
    initial_max_cols = pd.get_option('display.max_columns')
    initial_max_rows = pd.get_option('display.max_rows')
    initial_width = pd.get_option('display.width')

    # Reformat displays
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows',None)
    if display_width is not None:
            pd.set_option('display.width',display_width)

    #Output information to print line or file
    if output_file is None:
         for title, value in output:
            print(title_line(title))
            print(value)
    else:
        try:
            with open(output_file,'x' if output_safe else 'w') as file:
                for title, value in output:
                    file.write(title_line(title))
                    file.write(str(value) + '\n')
        except FileExistsError:
            print("Nothing outputted: file '{}' already exists".format(output_file))
    # Reset display settings
    pd.set_option('display.max_columns', initial_max_cols)
    pd.set_option('display.max_columns', initial_max_rows)
    pd.set_option('display.max_columns', initial_width)

# Setup helper methods. All of these return the value to display

def preview(df,preview_rows,preview_max_cols):
    """ Returns a preview of a dataframe, which contains both header
    rows and tail rows.
    """
    assert type(df) is pd.DataFrame
    if preview_rows <= 0:
        preview_rows = 1
    initial_max_cols = pd.get_option('display.max_columns')
    pd.set_option('display.max_columns', preview_max_cols)
    data = str(df.iloc[np.r_[0:preview_rows,-preview_rows:0]])
    pd.set_option('display.max_columns', initial_max_cols)
    return data

def get_info(df, verbose = None,max_cols = None, memory_usage = None, null_counts = None):
    """ Returns the .info() output of a dataframe
    """
    assert type(df) is pd.DataFrame
    buffer = io.StringIO()
    df.info(verbose, buffer, max_cols, memory_usage, null_counts)
    return buffer.getvalue()

def percentiles(df):
    """ Takes a dataframe and returns the quartiles for each column,
    or an error message if there are no columns with quantitative data.
    """
    assert type(df) is pd.DataFrame
    try:
        return df.quantile(q = [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1])
    except ValueError:
        return None#"No columns with numeric data."

def data_types(df):
    """ Takes in a dataframe and returns a dataframe with
    information on the data-types present in each column.
    """
    assert type(df) is pd.DataFrame
    output_df = pd.DataFrame([])
    row_count = df.shape[0]
    row_indexes = ['rows_numerical','rows_string','rows_date_time','category_count','largest_category','rows_na','rows_total']
    for colname in df:
        data = df[colname] # data is the pandas series associated with this column

        # number of numerical values in the column
        rows_numerical = pd.to_numeric(data,errors = 'coerce').count()

        # number of values that can't be coerced to a numerical
        rows_string = row_count - rows_numerical

        # number of values that can be coerced to a date-time object
        rows_date_time = pd.to_datetime(data,errors = 'coerce',infer_datetime_format = True).count()

        # categories in column
        value_counts = data.value_counts()

        # number of different values in the dataframe
        categories = data.value_counts().count()

        # largest category
        largest_category = value_counts[0]

        # number of null/missing values
        rows_na = data.isnull().sum()

        # build the output list
        output_data = [rows_numerical, rows_string, rows_date_time, categories, largest_category,rows_na,row_count]

        # format the output
        for index in range(7):
            output_data[index] = format_row_number(output_data[index],row_count)

        # add to dataframe
        output_df.loc[:,colname] = pd.Series(output_data)

    # row names
    output_df.index = row_indexes
    return output_df.transpose()

def format_row_number(rows, total_rows):
    return "{} ({}%)".format(rows, round(rows/total_rows*100,2))

# Utility methods

def title_line(text):
    """Returns a string that represents the
    text as a title blurb
    """
    columns = shutil.get_terminal_size()[0]
    start = columns // 2 - len(text) // 2
    output = '='*columns + '\n\n' + \
            ' ' * start + str(text) + "\n\n" + \
            '='*columns + '\n'
    return output

def try_except(function,*args):
    """ Tries a function and catches all exceptions"""
    try:
        return function(*args)
    except BaseException:
        return None

