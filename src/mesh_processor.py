import trimesh


class MeshProcessor:
    @staticmethod
    def otimizar_para_venda(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Aplica otimizações para deixar o modelo pronto para venda."""
        print("🔧 Otimizando modelo...")
        
        # Faz uma cópia para não alterar o original
        mesh = mesh.copy()
        
        # 1. Remove vértices duplicados
        mesh.merge_vertices()
        
        # 2. Remove faces degeneradas (triângulos com área zero)
        mesh.remove_degenerate_faces()
        
        # 3. Preenche buracos (se houver)
        if not mesh.is_watertight:
            try:
                mesh.fill_holes()
            except:
                print("   ⚠️ Não foi possível preencher buracos automaticamente")
        
        # 4. Suaviza superfícies (apenas se tiver faces)
        if len(mesh.faces) > 0:
            try:
                # Filtro Laplaciano simples para suavizar
                mesh = mesh.smoothed()
            except:
                print("   ⚠️ Suavização não aplicada")
        
        # 5. Reduz polígonos (decimação) se tiver muitos
        if len(mesh.faces) > 10000:
            try:
                mesh = mesh.simplify_quadric_decimation(10000)
            except:
                print("   ⚠️ Decimação não aplicada")
        
        # 6. Ajusta base para ficar plana (z = 0)
        bounds = mesh.bounds
        z_min = bounds[0][2]
        for i, vertex in enumerate(mesh.vertices):
            if abs(vertex[2] - z_min) < 0.001:
                mesh.vertices[i][2] = 0
        
        # 7. Centraliza o modelo no eixo X e Y (mantém Z)
        centroid = mesh.centroid
        mesh.apply_translation([-centroid[0], -centroid[1], 0])
        
        print("✅ Modelo otimizado!")
        return mesh