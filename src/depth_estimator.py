import numpy as np
import torch
from PIL import Image
from transformers import DPTForDepthEstimation, DPTImageProcessor


class DepthEstimator:
    def __init__(self):
        print("🔄 Carregando modelo de profundidade...")
        self.processor = DPTImageProcessor.from_pretrained("Intel/dpt-hybrid-midas")
        self.model = DPTForDepthEstimation.from_pretrained("Intel/dpt-hybrid-midas")
        self.model.eval()
        print("✅ Modelo carregado!")
    
    def estimar_profundidade(self, caminho_imagem: str) -> np.ndarray:
        """Gera mapa de profundidade a partir de uma imagem."""
        print("📷 Processando imagem...")
        
        # Abre a imagem
        imagem = Image.open(caminho_imagem)
        
        # Redimensiona para 512x512 (limite de memória)
        imagem = imagem.resize((512, 512))
        
        # Pré-processa
        inputs = self.processor(images=imagem, return_tensors="pt")
        
        # Gera profundidade
        with torch.no_grad():
            outputs = self.model(**inputs)
            depth = outputs.predicted_depth
        
        # Converte para numpy e normaliza
        depth = depth.squeeze().cpu().numpy()
        depth = (depth - depth.min()) / (depth.max() - depth.min()) * 255
        depth = depth.astype(np.uint8)
        
        print("✅ Profundidade gerada!")
        return depth