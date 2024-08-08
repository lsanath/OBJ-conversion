import SimpleITK as sitk
import numpy as np
from skimage import measure
import trimesh
import os


def load_image(file_path):
    image = sitk.ReadImage(file_path)
    array = sitk.GetArrayFromImage(image)
    spacing = image.GetSpacing()
    return array, spacing


def save_to_obj(vertices, faces, vertex_colors, output_file):
    # Create a trimesh object
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, vertex_colors=vertex_colors)
    # Export the mesh to OBJ format
    mesh.export(output_file)


def process_file(file_path, output_path, level=0.5):
    array, spacing = load_image(file_path)

    # Normalize spacing to get aspect ratio
    spacing = np.array(spacing)
    normalized_spacing = spacing / np.min(spacing)

    # Extract isosurface
    vertices, faces, _, _ = measure.marching_cubes(array, level=level, spacing=normalized_spacing)

    # Assuming array contains RGB data, you need to extract color information
    if array.ndim == 4 and array.shape[-1] == 3:
        # Normalize vertex positions to array indices
        vertex_indices = (vertices / normalized_spacing).astype(int)
        vertex_colors = array[vertex_indices[:, 0], vertex_indices[:, 1], vertex_indices[:, 2], :]
    else:
        vertex_colors = np.ones((vertices.shape[0], 3), dtype=np.uint8) * 255  # default to white

    save_to_obj(vertices, faces, vertex_colors, output_path)
    print(f"Saved {file_path} to {output_path}")


def convert_folder_to_obj(input_folder, output_folder, level=0.5):
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.nrrd') or file.endswith('.nii') or file.endswith('.nii.gz'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_folder)
                output_file = os.path.splitext(relative_path)[0] + '.obj'
                output_path = os.path.join(output_folder, output_file)

                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                process_file(file_path, output_path, level=level)


# Example usage
input_folder = r"D:\LiverVision-Study Malcolm\Waitemata LiverVision"
output_folder = r"D:\LiverVision-Study Malcolm\output obj"
convert_folder_to_obj(input_folder, output_folder, level=0.5)
