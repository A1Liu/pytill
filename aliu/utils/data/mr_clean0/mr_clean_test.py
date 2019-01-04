# -*- coding: utf-8 -*-
import mr_clean_utils as mcu

def scrub_str_cols0(df,column,char_scrub_cutoff): 
    # Tries to remove common characters from the front of the strings in df[column]
    if not mcu.is_num(df[column]): # if it's not a numeric
        char_scrub_cutoff = mcu.get_cutoff(column, char_scrub_cutoff)
        from_front = ""
        from_back = ""
        flag1 = True
        flag2 = True
        while flag1 or flag2:
            valcounts = df[column].str[0].value_counts()
            flag1 = valcounts[0] > char_scrub_cutoff * df.shape[0]
            if flag1:
                from_front+=valcounts.index[0]
                df[column] = df[column].str[1:]
            valcounts = df[column].str[-1].value_counts()
            flag2 = valcounts[0] > char_scrub_cutoff * df.shape[0]
            if flag2:
                from_back=valcounts.index[0]+from_back
                df[column] = df[column].str[:-1]
        if len(from_front) > 0 or len(from_back) > 0:
           return (from_front, from_back, column)

def scrub_str_cols(df,column,char_scrub_cutoff): 
    # Tries to remove common characters from the front of the strings in df[column]
    if not mcu.is_num(df[column]): # if it's not a numeric
        char_scrub_cutoff = mcu.get_cutoff(column, char_scrub_cutoff)
        from_front,from_back = "",""
        flag1, flag2 = True,True
        capture1,capture2 = mcu.ic_vec(df),mcu.ic_vec(df) # Boolean column vectors
        iteration = 0
        get_colname = mcu.get_colname_gen(df)
        
        while flag1 or flag2:
            
            valcounts = df.loc[capture1 >= iteration,column].str[0].value_counts()
            flag1 = valcounts[0] > char_scrub_cutoff * mcu.rows(df)
            if flag1:
                from_front+=valcounts.index[0]
                capture1 =df[column].str.startswith(valcounts.index[0])&(capture1 >= iteration)
                df.loc[capture1,column] = df.loc[capture1,column].str[1:]
                capture1+=1
                
            
            valcounts = df.loc[capture2 >= iteration,column].str[-1].value_counts()
            flag2 = valcounts[0] > char_scrub_cutoff * mcu.rows(df)
            if flag2:
                from_back=valcounts.index[0]+from_back
                capture2 =df[column].str.endswith(valcounts.index[0])&capture2
                df.loc[capture2,column] = df.loc[capture2,column].str[:-1]
                capture2+=1
            iteration+=1
            
            
        if len(from_front + from_back) > 0:
            # Generate unique column names for each appended column
            bool_col_1 = next(get_colname(column+'_scrubf'))
            bool_col_2 = next(get_colname(column+'_scrubb'))
            df[bool_col_1] = capture1 # Add columns
            df[bool_col_2] = capture2 # Add columns
            return (from_front, from_back, column,bool_col_1,bool_col_2)