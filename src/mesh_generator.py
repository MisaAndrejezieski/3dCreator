import numpy as np
import trimesh
from scipy.spatial import Delaunay


class MeshGenerator:
    def __init__(self, escala_z: float = 2.0):
        self.escala_z = escala_z
    
    def profundidade_para_malha(self, depth_map: np.ndarray) -> trimesh.Trimesh:
        """Converte mapa de profundidade em malha 3D."""
        print("🔨 Gerando malha 3D...")
        
        h, w = depth_map.shape
        
        # Cria grid de coordenadas (x, y)
        x = np.linspace(0, w, w)
        y = np.linspace(0, h, h)
        x, y = np.meshgrid(x, y)
        
        # Aplica profundidade como altura (z)
        z = depth_map * self.escala_z
        
        # Cria vértices
        vertices = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)
        
        # Cria faces (triângulos)
        points_2d = vertices[:, :2]
        triang = Delaunay(points_2d)
        faces = triang.simplices
        
        # Cria malha
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        print("✅ Malha gerada!")
        return mesh