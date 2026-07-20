import trimesh


class MeshProcessor:
    @staticmethod
    def otimizar_para_venda(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Aplica otimizações para deixar o modelo pronto para venda."""
        print("🔧 Otimizando modelo...")
        
        # 1. Remove faces duplicadas e degeneradas
        mesh.remove_duplicate_faces()
        mesh.remove_degenerate_faces()
        
        # 2. Preenche buracos
        if len(mesh.faces) > 0:
            mesh.fill_holes()
        
        # 3. Suaviza superfícies
        mesh = mesh.smoothed()
        
        # 4. Reduz polígonos (decimação) sem perder detalhes
        if len(mesh.faces) > 10000:
            mesh = mesh.simplify_quadric_decimation(10000)
        
        # 5. Ajusta base para ficar plana
        bounds = mesh.bounds
        z_min = bounds[0][2]
        for i, vertex in enumerate(mesh.vertices):
            if vertex[2] == z_min:
                mesh.vertices[i][2] = 0
        
        # 6. Centraliza o modelo
        mesh.apply_translation(-mesh.centroid)
        
        print("✅ Modelo otimizado!")
        return mesh