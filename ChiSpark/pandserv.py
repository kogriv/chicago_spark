import pandas as pd
import sys
from IPython.display import display, HTML

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
    Format a pandas DataFrame by inserting a separator symbol in numeric values, 
    rounding float values, and truncating string values.

    Args:
        df (pd.DataFrame): The DataFrame to format.
        sep (str): The separator symbol to insert in numeric values (e.g., ',' or "'").
        round_num (int): The number of decimal places to round float values.
        round_str (int): The maximum length to truncate string values to.
    
    Returns:
        pd.DataFrame: The formatted DataFrame.
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
    """
    Format a numeric value by inserting a separator
    symbol and rounding to a specified number of decimal places.

    Args:
        val (int or float): The numeric value to format.
        sep (str, optional): The separator symbol to insert
                            in the formatted value (e.g., ',' or "'").
                            Defaults to "'".
        round_num (int, optional): The number of decimal
                            places to round the value. Defaults to 0.

    Returns:
        str: The formatted numeric value as a string.
    """
    if not isinstance(val, (int, float)):
        raise ValueError("The value must be an integer or a float")
    
    return ('{:,.%df}' % round_num).format(val).replace(',', sep)

def inventory_objects():
    """
    Create a DataFrame containing the names, types, and sizes of objects 
    in the current global namespace, excluding special objects.

    Returns:
        pd.DataFrame: A DataFrame with columns ['Name', 'Type', 'Size (bytes)']
    """
    # List to store information about objects
    inventory = []
    
    # Iterate over all objects in the current namespace
    for name, obj in globals().items():
        if not name.startswith('__'):  # Ignore special objects
            obj_type = type(obj).__name__
            obj_size = sys.getsizeof(obj)
            inventory.append([name, obj_type, obj_size])
    
    # Create DataFrame to represent data in table format
    df = pd.DataFrame(inventory, columns=['Name', 'Type', 'Size (bytes)'])
    
    # Sort by object size
    df = df.sort_values(by='Size (bytes)', ascending=False).reset_index(drop=True)
    
    return df

def display_chunked(df, chunk_size=10, pages=1):
    """
    Display a DataFrame in chunks, with the ability to paginate through the rows.
    By default, it displays only the first page unless more pages are specified.

    Args:
        df (pd.DataFrame): The DataFrame to display.
        chunk_size (int): The number of rows per chunk. Defaults to 10.
        pages (int): The number of pages to display. Defaults to 1.
    """
    total_rows = len(df)
    for page in range(pages):
        start = page * chunk_size * 2
        end = min(start + chunk_size * 2, total_rows)
        
        # Split into two blocks
        df1 = df.iloc[start:start + chunk_size]
        df2 = df.iloc[start + chunk_size:end]
        
        # Combine tables side by side
        html = '<div style="display: flex; justify-content: space-between;">'
        html += '<div style="flex: 1; padding-right: 10px;">{}</div>'.format(df1.to_html(index=False))
        html += '<div style="flex: 1; padding-left: 10px;">{}</div>'.format(df2.to_html(index=False))
        html += '</div>'
        
        display(HTML(html))
        
        print(f"Displaying rows {start} to {min(start + chunk_size * 2 - 1, total_rows - 1)} of {total_rows}")
        
        if pages > 1:
            user_input = input("Press Enter to continue or 'q' to quit: ")
            if user_input.lower() == 'q':
                print("Terminating the display.")
                break