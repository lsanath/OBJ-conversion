import SimpleITK as sitk
import numpy as np
from skimage import measure
import trimesh
import os


def load_nrrd(file_path):
    # Load the NRRD file
    image = sitk.ReadImage(file_path)
    array = sitk.GetArrayFromImage(image)
    spacing = np.array(image.GetSpacing())  # Get voxel spacing
    origin = np.array(image.GetOrigin())  # Get image origin
    return array, spacing, origin


def convert_to_stl(vertices, faces, output_file):
    # Create a mesh object using vertices and faces
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    # Export the mesh to STL format
    mesh.export(output_file)
    print(f"Saved STL file: {output_file}")


def process_nrrd_to_stl(file_path, output_path, level=0.5):
    # Load the NRRD file and get the array, spacing, and origin
    array, spacing, origin = load_nrrd(file_path)

    # Normalize the spacing to match the original voxel dimensions
    vertices, faces, _, _ = measure.marching_cubes(array, level=level, spacing=spacing)

    # Adjust the vertices by adding the origin to match the original coordinates
    vertices += origin

    # Convert to STL and save
    convert_to_stl(vertices, faces, output_path)


def convert_folder_nrrd_to_stl(input_folder, output_folder, level=0.5):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.nrrd'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_folder)
                output_file = os.path.splitext(relative_path)[0] + '.stl'
                output_path = os.path.join(output_folder, output_file)

                # Ensure the output subdirectories exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Convert the NRRD file to STL
                process_nrrd_to_stl(file_path, output_path, level=level)


# Example usage
input_folder = r"D:\LiverVision-Study Malcolm\Waitemata LiverVision"
output_folder = r"D:\LiverVision-Study Malcolm\output stl cordinates"
convert_folder_nrrd_to_stl(input_folder, output_folder, level=0.5)

