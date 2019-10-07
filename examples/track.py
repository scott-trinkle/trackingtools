import trackingtools as tools

# In this example, I will be tracking experiment 4 from the xray data,
# converting the streamlines to a track density image, and warping that
# track density image into the Allen atlas space

# First, I will run the tractography with all of the relevant parameters:
tools.track(modality="xray",  # must be "xray" or "mri"
            exp_id=4,  # experiment ID, from 1-10
            # note that output filenames must end in ".tck"
            tracks="test_xray_tracks_exp4.tck",
            select=10000,  # this is the number of seeds
            step=0.0375,  # step size in mm
            curvature=35,  # curvature in um, value from Aydogan paper
            minlength=0.75,  # minimum streamline length in mm
            maxlength=38.0,  # maximum streamline length in mm
            cutoff=0.05)  # odf cutoff value

# This will start the MRtrix tracking algorithm, with a live percent update

# Once this is finished, we can map the streamlines to a tract density image
# tools.map
tools.map_to_density(modality="xray",
                     tracks="test_xray_tracks_exp4.tck",
                     output="test_xray_tracks_exp4_density.nii.gz")

# And then we can warp the density map into the allen reference space
tools.register(input_fn="test_xray_tracks_exp4_density.nii.gz",
               output_fn="test_xray_tracks_exp4_density_allen_space.nii.gz",
               input_modality="xray",
               output_modality="allen",
               verbose=1)
