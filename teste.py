import trimesh

# Carrega o GLB
cena = trimesh.load("outputs/425.glb")

# Verifica se é uma cena ou uma malha única
if isinstance(cena, trimesh.Scene):
    print("📦 O arquivo é uma cena com múltiplos objetos.")
    # Extrai todas as geometrias da cena
    mesh = trimesh.util.concatenate([geom for geom in cena.geometry.values()])
    print(f"✅ Objetos na cena: {len(cena.geometry)}")
else:
    mesh = cena

print(f"✅ Vértices: {len(mesh.vertices)}")
print(f"✅ Faces: {len(mesh.faces)}")
print(f"✅ É uma malha fechada? {mesh.is_watertight}")
print(f"✅ Volume: {mesh.volume:.4f}")
print(f"✅ Área da superfície: {mesh.area:.4f}")

# Tenta exportar como PLY para teste
mesh.export("outputs/425_test.ply")
print("✅ Arquivo PLY exportado: outputs/425_test.ply")