import pandas as pd


def read_csv(fn):
    '''
    Convenience function to read a csv file into a Pandas dataframe.

    Parameters
    __________
    fn : str
        Filename for the csv file

    Returns
    _______
    df : pd.DataFrame
        Pandas dataframe

    Example
    _______
    >> df = read_csv(fn='dmri_results.csv')
    '''
    df = pd.read_csv(fn)
    return df
