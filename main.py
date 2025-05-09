#gpt edited code for better readability and structure
import cv2
import matplotlib.pyplot as plt
from rembg import remove
import trimesh
from shapely.geometry import Polygon

def process_image_to_3d(image_path: str, extrusion_height=50.0, export_path='output.obj'):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    output = remove(img)
    if output.shape[2] == 4:
        output = output[..., :3]

    plt.imshow(output)
    plt.axis('off')
    plt.title("Background Removed")
    plt.show()

    gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        raise RuntimeError("No object found in image.")

    contour = max(contours, key=cv2.contourArea).squeeze()

    polygon = Polygon(contour)
    path = trimesh.load_path(polygon.exterior.coords)
    extruded_mesh = path.extrude(height=extrusion_height)
    extruded_mesh.export(export_path)

    return extruded_mesh

if __name__ == "__main__":
    img_path = input("Enter image path (e.g., chair.png): ").strip()
    mesh = process_image_to_3d(img_path, export_path='output.obj')