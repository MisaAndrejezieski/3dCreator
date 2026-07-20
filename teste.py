import trimesh

# Carrega o GLB
mesh = trimesh.load("outputs/425.glb")

print(f"✅ Vértices: {len(mesh.vertices)}")
print(f"✅ Faces: {len(mesh.faces)}")
print(f"✅ É uma malha fechada? {mesh.is_watertight}")
print(f"✅ Volume: {mesh.volume}")
print(f"✅ Área: {mesh.area}")

# Tenta exportar como PLY (formato universal)
mesh.export("outputs/425_test.ply")
print("✅ Arquivo PLY exportado para teste: outputs/425_test.ply")