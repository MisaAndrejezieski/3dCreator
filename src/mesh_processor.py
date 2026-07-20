import numpy as np
import trimesh


class MeshProcessor:
    @staticmethod
    def otimizar_para_venda(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Aplica otimizações básicas para deixar o modelo pronto para venda."""
        print("🔧 Otimizando modelo...")
        
        # Faz uma cópia para não alterar o original
        mesh = mesh.copy()
        
        # 1. Remove vértices duplicados (esse método existe)
        mesh.merge_vertices()
        
        # 2. Remove faces degeneradas (usa o método que existe)
        try:
            faces_validas = mesh.nondegenerate_faces()
            if len(faces_validas) < len(mesh.faces):
                mesh.update_faces(faces_validas)
                print(f"   ✅ {len(mesh.faces)} faces restantes")
        except:
            print("   ⚠️ Pulando remoção de faces degeneradas")
        
        # 3. Preenche buracos (se houver)
        if not mesh.is_watertight:
            try:
                mesh.fill_holes()
                print("   ✅ Buracos preenchidos")
            except:
                print("   ⚠️ Pulando preenchimento de buracos")
        
        # 4. Suaviza (se possível)
        try:
            if len(mesh.faces) > 0:
                mesh = mesh.smoothed()
                print("   ✅ Superfície suavizada")
        except:
            print("   ⚠️ Pulando suavização")
        
        # 5. Ajusta base para ficar plana (z = 0)
        vertices = mesh.vertices.copy()
        z_min = vertices[:, 2].min()
        vertices[:, 2] = vertices[:, 2] - z_min
        mesh.vertices = vertices
        
        # 6. Centraliza no eixo X e Y (mantém Z)
        centroid = mesh.centroid
        mesh.apply_translation([-centroid[0], -centroid[1], 0])
        
        print("✅ Modelo otimizado!")
        return mesh