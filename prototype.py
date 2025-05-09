
# %%
#real code written manually
# %%
import cv2

# %%
path = 'fruit.jpg'

img = cv2.imread(path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# %%
from rembg import remove
output = remove(img)

if output.shape[2] == 4:
    output = output[..., :3]

# # %%
# output = cv2.resize(output, (600, 400))
# %%
import matplotlib.pyplot as plt

plt.imshow(output)
plt.axis('off')
plt.show()


# %%
import torch
model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")

# %%
model.eval()
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.small_transform
img1 = transform(output)
with torch.no_grad():
    depth = model(img1)

depth = torch.nn.functional.interpolate(
    depth.unsqueeze(1),
    size=output.shape[:2],
    mode="bicubic",
    align_corners=False,
).squeeze().numpy()

# %%
import matplotlib.pyplot as plt

plt.imshow(depth, cmap='plasma') 
plt.colorbar() 
plt.show()


# # %%
# # depth = cv2.resize(depth, (1440, 960), interpolation=cv2.INTER_AREA)

# depth.shape, resized.shape, output.shape

# %%
import trimesh
import shapely
from shapely.geometry import Polygon

gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
_, binary = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contour = max(contours, key=cv2.contourArea)
contour = contour.squeeze() 

polygon = Polygon(contour)

path = trimesh.load_path(polygon.exterior.coords)

extruded_mesh = path.extrude(height=200.0)

# %%
extruded_mesh.export('output.obj')

# %%
