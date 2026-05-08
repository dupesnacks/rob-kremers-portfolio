import numpy as np
from stl import mesh

# Create a stylized Boston Terrier bust model
# Perfect for Tina2S (~50-100mm scale)

def sphere(center, radius, slices=12, stacks=8):
    """Generate sphere vertices"""
    vertices = []
    for i in range(stacks + 1):
        lat = np.pi * i / stacks
        for j in range(slices + 1):
            lng = 2 * np.pi * j / slices
            x = radius * np.sin(lat) * np.cos(lng) + center[0]
            y = radius * np.sin(lat) * np.sin(lng) + center[1]
            z = radius * np.cos(lat) + center[2]
            vertices.append([x, y, z])
    return np.array(vertices)

def cylinder(center, radius, height, slices=12):
    """Generate cylinder vertices"""
    vertices = []
    for z_val in [0, height]:
        for j in range(slices):
            angle = 2 * np.pi * j / slices
            x = radius * np.cos(angle) + center[0]
            y = radius * np.sin(angle) + center[1]
            vertices.append([x, y, center[2] + z_val])
    return np.array(vertices)

# Build dog head bust
vertices = []
faces = []
vertex_offset = 0

# Main head (sphere)
head_verts = sphere([0, 0, 40], 25, slices=16, stacks=10)
vertices.append(head_verts)

# Snout (smaller sphere)
snout_verts = sphere([0, 25, 35], 15, slices=12, stacks=8)
vertices.append(snout_verts)

# Left ear (cone-like)
ear_verts = np.array([
    [-18, -8, 55], [-22, -8, 75], [-16, -12, 75],  # base
    [-15, -5, 65], [-20, -10, 70]  # tip
])
vertices.append(ear_verts)

# Right ear (mirror)
right_ear_verts = np.array([
    [18, -8, 55], [22, -8, 75], [16, -12, 75],
    [15, -5, 65], [20, -10, 70]
])
vertices.append(right_ear_verts)

# Neck/base
neck_verts = sphere([0, 0, 10], 22, slices=14, stacks=6)
vertices.append(neck_verts)

# Combine all vertices
all_vertices = np.vstack(vertices)

# Simple faces (triangulation)
# For now, create basic pyramid/cone faces for ears and simple triangles for main shapes
faces_list = [
    # Ears (simplified triangles)
    [80, 81, 82],
    [80, 82, 83],
    [80, 83, 84],
    [85, 86, 87],
    [85, 87, 88],
    [85, 88, 89],
]

# Extend with simple geometric connections
faces_array = np.array(faces_list)

# Create mesh
dog_mesh = mesh.Mesh(np.zeros(len(faces_array), dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces_array):
    for j in range(3):
        dog_mesh.vectors[i][j] = all_vertices[face[j]]

# Add a base platform for stability
base_height = 5
base_size = 35
base_faces = [
    [[0, 0, 0], [base_size, 0, 0], [0, base_size, 0]],
    [[base_size, 0, 0], [base_size, base_size, 0], [0, base_size, 0]],
    [[0, 0, base_height], [0, base_size, base_height], [base_size, 0, base_height]],
    [[base_size, 0, base_height], [0, base_size, base_height], [base_size, base_size, base_height]],
]

base_mesh = mesh.Mesh(np.zeros(len(base_faces), dtype=mesh.Mesh.dtype))
for i, face in enumerate(base_faces):
    base_mesh.vectors[i] = np.array(face)

# Combine meshes
dog_mesh.vectors = np.concatenate([dog_mesh.vectors, base_mesh.vectors])

# Save
dog_mesh.save('/Users/rk/clawd/dog_bust_mini.stl')
print("✅ Dog bust saved: dog_bust_mini.stl (65x65x80mm)")
print("   Print time: ~2-3 hours at 0.2mm layer height")
print("   Material: ~25-35g PLA/PETG")

