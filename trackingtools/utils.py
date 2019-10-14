import numpy as np
import pandas as pd
import nibabel as nib
import pkg_resources
data_path = pkg_resources.resource_filename('trackingtools', 'data/')


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


def get_projection(ID, trimmed=False, both=False, data_only=True):
    img = nib.load(
        data_path + f'allen/projection_densities/I{ID}_density.nii.gz')
    projection_density = img.get_data()

    if trimmed:
        timg = nib.load(data_path + f'allen/truth_masks/I{ID}_truth.nii.gz')
        mask = timg.get_data()
        trimmed = np.zeros_like(projection_density)
        trimmed[mask == 1] = projection_density[mask == 1]

        if both:
            if data_only:
                return projection_density, trimmed
            else:
                img, projection_density, trimmed
        else:
            if data_only:
                return trimmed
            else:
                img, trimmed
    else:
        if data_only:
            return projection_density
        else:
            return img, projection_density


def get_brain_mask():
    img = nib.load(data_path + 'allen/brain_mask.nii.gz')
    data = img.get_data()
    return data
