import numpy as np
import subprocess
import pkg_resources
data_path = pkg_resources.resource_filename('trackingtools', 'data/')


def track(modality, exp_id, tracks, algorithm='iFOD2', select=500000,
          step=0.0375, curvature=35, minlength=0.75,
          maxlength=38.0, cutoff=0.05, nthreads=4, force=False):
    '''
    See documentation at:
    https://mrtrix.readthedocs.io/en/latest/reference/commands/tckgen.html

    Relevant parameters:
    ____________________
    modality: str
        "xray" or "mri
    exp_id : int
        Allen experiment ID, 1-10
    tracks : str
        Output tractogram filename. Must end in ".tck"
    select : int
        Number of seeds
    step : float
        Step size in mm
    curvature : float
        Curvature in um. Converted to angle automatically.
    cutoff : float
        Cutoff ODF value
    force : bool
        Force override an existing tract file. Default is False. 
    '''

    source = data_path + f'{modality}/{modality}_odfs.nii.gz'
    seed_image = data_path + f'{modality}/seed_images/I{exp_id}.nii.gz'

    # From Aydogan paper, using same radius of curvature
    angle = 2 * np.arcsin(step * 1000 / (2 * curvature)) * 180 / np.pi

    track_call = ['tckgen',
                  '-algorithm', algorithm,
                  '-select', f'{select}',
                  '-minlength', f'{minlength}',
                  '-maxlength', f'{maxlength}',
                  '-step', f'{step}',
                  '-cutoff', f'{cutoff}',
                  '-angle', f'{angle}',
                  '-seed_rejection', seed_image,
                  '-nthreads', f'{nthreads}']
    if force:
        track_call.append('-force')
    track_call.append(source)
    track_call.append(tracks)

    subprocess.run(track_call)


def map_to_density(modality, tracks, output, weights_path=None,
                   vox=0.05, nthreads=4):
    '''
    See documentation at
    https://mrtrix.readthedocs.io/en/latest/reference/commands/tckmap.html

    Relevant parameters:
    ____________________
    modality : str
        "xray" or "mri"
    tracks : str
        Input tractogram filename. Must end in ".tck"
    output : str
        Output track density filename. Must end in ".nii.gz"
    weights_path : str
        Filename for filtered streamline weights, if applicable.
    vox : float
        Voxel size of template image in mm. Should always be 0.05
    '''
    template_image = data_path + f'{modality}/{modality}_template.nii.gz'

    map_call = ['tckmap',
                '-template', template_image,
                '-vox', f'{vox}',
                '-precise',
                '-nthreads', f'{nthreads}']
    if weights_path is not None:
        map_call.append('-tck_weights_in')
        map_call.append(weights_path)
    map_call.append(tracks)
    map_call.append(output)

    subprocess.run(map_call)


def sift_streamlines(in_tracks, out_weights, modality, nthreads=4):
    '''
    See documentation at
    https://mrtrix.readthedocs.io/en/latest/reference/commands/tcksift2.html

    Relevant parameters:
    ____________________
    in_tracks : str
        Input tracogram filename, ends in ".tck"
    out_weights : str
        Output streamline weights file, ends in ".txt"
    modality : str
        "xray" or "mri"
    '''

    in_fod = data_path + f'{modality}/{modality}_odfs.nii.gz'

    sift_call = ['tcksift2',
                 '-nthreads', f'{nthreads}']

    sift_call.append(in_tracks)
    sift_call.append(in_fod)
    sift_call.append(out_weights)

    subprocess.run(sift_call)
