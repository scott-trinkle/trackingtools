import subprocess
import pkg_resources
data_path = pkg_resources.resource_filename('trackingtools', 'data/')

all2mri = [data_path + 'transforms/allen_to_mri_warp.nii.gz',
           data_path + 'transforms/allen_to_mri_affine.mat']
mri2all = ['[' + data_path + 'transforms/allen_to_mri_affine.mat, 1]',
           data_path + 'transforms/allen_to_mri_invwarp.nii.gz']
xray2mri = [data_path + 'transforms/xray_to_mri_warp.nii.gz',
            data_path + 'transforms/xray_to_mri_affine.mat']
mri2xray = ['[' + data_path + 'transforms/xray_to_mri_affine.mat, 1]',
            data_path + 'transforms/xray_to_mri_invwarp.nii.gz']


def register(input_fn, output_fn, input_modality, output_modality, verbose=0):
    '''
    Parameters
    __________
    input_fn : str
        Input filename to transform, ends in ".nii.gz"
    output_fn : str
        Output filename for result, ends in ".nii.gz"
    input_modality : str
        Modality for input_fn. "xray", "mri", or "allen".
    output_modality : str
        Modality for output_fn. "xray", "mri", or "allen".
    verbose : int
        1 to print info about the registration, 0 to hide it. Default is 0. 
    '''
    ref = data_path + f'{output_modality}/{output_modality}_template.nii.gz'
    if input_modality == 'allen':
        if output_modality == 'mri':
            transforms = all2mri
        if output_modality == 'xray':
            transforms = mri2xray + all2mri
    if input_modality == 'xray':
        if output_modality == 'allen':
            transforms = mri2all + xray2mri
        if output_modality == 'mri':
            transforms = xray2mri
    if input_modality == 'mri':
        if output_modality == 'allen':
            transforms = mri2all
        if output_modality == 'xray':
            transforms = mri2xray

    antscall = ['antsApplyTransforms',
                '-d', '3',
                '-e', '0',
                '-i', input_fn,
                '-o', output_fn,
                '-r', ref,
                '-v', f'{verbose}']
    for transform in transforms:
        antscall.append('-t')
        antscall.append(transform)

    return antscall

    subprocess.run(antscall)
