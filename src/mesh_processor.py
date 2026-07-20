import numpy as np
import trimesh


class MeshProcessor:
    @staticmethod
    def otimizar_para_venda(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Aplica otimizações básicas para deixar o modelo pronto para venda."""
        print("🔧 Otimizando modelo...")
        
        # Faz uma cópia para não alterar o original
        mesh = mesh.copy()
        
        # 1. Remove vértices duplicados
        mesh.merge_vertices()
        
        # 2. Remove faces degeneradas (usa o método correto)
        faces_validas = mesh.nondegenerate_faces()
        mesh.update_faces(faces_validas)
        
        # 3. Remove faces duplicadas (usa merge_vertices + update_faces)
        mesh.merge_vertices()
        # Remove faces que compartilham todos os vértices
        mesh.remove_duplicate_faces()
        
        # 4. Preenche buracos (se houver)
        if not mesh.is_watertight:
            try:
                mesh.fill_holes()
                print("   ✅ Buracos preenchidos")
            except:
                print("   ⚠️ Pulando preenchimento de buracos")
        
        # 5. Suaviza (se possível)
        try:
            mesh = mesh.smoothed()
            print("   ✅ Superfície suavizada")
        except:
            print("   ⚠️ Pulando suavização")
        
        # 6. Ajusta base para ficar plana (z = 0)
        vertices = mesh.vertices.copy()
        z_min = vertices[:, 2].min()
        vertices[:, 2] = vertices[:, 2] - z_min
        mesh.vertices = vertices
        
        # 7. Centraliza no eixo X e Y (mantém Z)
        centroid = mesh.centroid
        mesh.apply_translation([-centroid[0], -centroid[1], 0])
        
        print("✅ Modelo otimizado!")
        return mesh