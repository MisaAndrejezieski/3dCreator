import trimesh


class MeshProcessor:
    @staticmethod
    def otimizar_para_venda(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Aplica otimizações para deixar o modelo pronto para venda."""
        print("🔧 Otimizando modelo...")
        
        # Faz uma cópia para não alterar o original
        mesh = mesh.copy()
        
        # 1. Remove faces duplicadas e degeneradas
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        
        # 2. Preenche buracos (se houver)
        if mesh.is_watertight == False:
            mesh.fill_holes()
        
        # 3. Suaviza superfícies (apenas se tiver faces)
        if len(mesh.faces) > 0:
            mesh = mesh.smoothed()
        
        # 4. Reduz polígonos (decimação) se tiver muitos
        if len(mesh.faces) > 10000:
            mesh = mesh.simplify_quadric_decimation(10000)
        
        # 5. Ajusta base para ficar plana (z = 0)
        bounds = mesh.bounds
        z_min = bounds[0][2]
        for i, vertex in enumerate(mesh.vertices):
            if abs(vertex[2] - z_min) < 0.001:  # Tolerância para ponto flutuante
                mesh.vertices[i][2] = 0
        
        # 6. Centraliza o modelo no eixo X e Y (mantém Z)
        centroid = mesh.centroid
        mesh.apply_translation([-centroid[0], -centroid[1], 0])
        
        print("✅ Modelo otimizado!")
        return mesh