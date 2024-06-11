import pandas as pd

def get_column_types(dataframe):
    """
    Define pandas data types
    Return dict {column_name:colunm_type (or dict {index:value_type})}
    """
    col_types = {}
    for column in dataframe.columns:
        col_types[column] = str(dataframe[column].dtype)
        if col_types[column] == 'object':
            column_values = dataframe[column]
            column_val_types = {}
            for idx, val in column_values.items():
                if isinstance(val, int):
                    column_val_types[idx] = 'int64'
                elif isinstance(val, float):
                    column_val_types[idx] = 'float64'
                elif isinstance(val, str):
                    column_val_types[idx] = 'string'
                else:
                    column_val_types[idx] = type(val).__name__ 
                col_types[column] = column_val_types
    return col_types

def get_df_formated(df, sep, round_num, round_str):
    """
    Process pandas df. Insert sep_symbol (like 1'000)
    Round float values
    Cut string values
    """
    for col in df.columns:
        if df[col].dtype == 'float64':
            for idx, val in df[col].items():
                if val % 1 == 0:
                        val = int(val)
                if isinstance(val, float):
                        df.loc[idx, col] = \
                            ('{:,.%df}' % round_num).format(val).replace(',', sep)
                elif isinstance(val, int):
                    df.loc[idx, col] = ('{:,.%df}' % 0).format(val).replace(',', sep)
        elif df[col].dtype == 'int64':
            df[col] = df[col].\
            apply(lambda x: ('{:,.%df}' % 0).format(x).replace(',', sep) \
                  if pd.notnull(x) else x)
        else:
            for idx, val in df[col].items():
                try:
                    val = float(val)
                    
                    if val % 1 == 0:
                        val = int(val)
                    if isinstance(val, float):
                        df.loc[idx, col] = ('{:,.%df}' % round_num).format(val).replace(',', sep)
                    elif isinstance(val, int):
                        df.loc[idx, col] = ('{:,.%df}' % 0).format(val).replace(',', sep)
                except ValueError:
                    df.loc[idx, col] = val[:round_str]

def gvf(val, sep="'", round_num=0):
    return ('{:,.%df}' % round_num).format(val).replace(',', sep)

def tstf():
    print("tstf")
    return