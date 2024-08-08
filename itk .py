import SimpleITK as sitk
import nibabel as nib
import numpy as np
import os


def nrrd_to_nifti(nrrd_filename, nifti_filename):
    # Read the NRRD file
    nrrd_image = sitk.ReadImage(nrrd_filename)

    # Get the numpy array from the NRRD image
    nrrd_array = sitk.GetArrayFromImage(nrrd_image)

    # Get the NRRD image metadata (spacing, origin, direction)
    spacing = nrrd_image.GetSpacing()
    origin = nrrd_image.GetOrigin()
    direction = nrrd_image.GetDirection()

    # Check if the image has multiple channels
    if nrrd_array.ndim == 4 and nrrd_array.shape[-1] == 3:
        # Split the channels
        r_channel = nrrd_array[..., 0]
        g_channel = nrrd_array[..., 1]
        b_channel = nrrd_array[..., 2]

        # Stack the channels to create a multi-channel NIfTI image
        stacked_array = np.stack([r_channel, g_channel, b_channel], axis=-1)

        # Create an affine matrix for the NIfTI image
        direction_matrix = np.array(direction).reshape(3, 3)
        affine = np.eye(4)
        affine[:3, :3] = np.diag(spacing).dot(direction_matrix)
        affine[:3, 3] = origin

        # Create a NIfTI image using the nibabel library
        nifti_image = nib.Nifti1Image(stacked_array, affine)
    else:
        # Create an affine matrix for the NIfTI image
        direction_matrix = np.array(direction).reshape(3, 3)
        affine = np.eye(4)
        affine[:3, :3] = np.diag(spacing).dot(direction_matrix)
        affine[:3, 3] = origin

        # Create a NIfTI image using the nibabel library
        nifti_image = nib.Nifti1Image(nrrd_array, affine)

    # Save the NIfTI image
    nib.save(nifti_image, nifti_filename)
    print(f"Successfully converted {nrrd_filename} to {nifti_filename}")


def convert_folder_nrrd_to_nifti(input_folder, output_folder):
    # Walk through the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.nrrd'):
                nrrd_filepath = os.path.join(root, file)

                # Construct the corresponding output file path
                relative_path = os.path.relpath(nrrd_filepath, input_folder)
                nifti_filename = os.path.splitext(relative_path)[0] + '.nii'
                nifti_filepath = os.path.join(output_folder, nifti_filename)

                # Ensure the output subdirectories exist
                os.makedirs(os.path.dirname(nifti_filepath), exist_ok=True)

                # Convert the file
                nrrd_to_nifti(nrrd_filepath, nifti_filepath)


# Example usage
input_folder = r"D:\LiverVision-Study Malcolm\Waitemata LiverVision"
output_folder = r"D:\LiverVision-Study Malcolm\Output nifti"
convert_folder_nrrd_to_nifti(input_folder, output_folder)
