import os
from src.depth_estimator import DepthEstimator
from src.mesh_generator import MeshGenerator
from src.mesh_processor import MeshProcessor

def processar_imagem(caminho_imagem: str):
    """Pipeline completo: imagem → modelo 3D otimizado."""
    
    print(f"\n📁 Processando: {caminho_imagem}")
    print("=" * 50)
    
    # 1. Estima profundidade
    depth_estimator = DepthEstimator()
    depth_map = depth_estimator.estimar_profundidade(caminho_imagem)
    
    # 2. Gera malha 3D
    mesh_generator = MeshGenerator(escala_z=2.0)
    mesh = mesh_generator.profundidade_para_malha(depth_map)
    
    # 3. Otimiza para venda
    mesh_processor = MeshProcessor()
    mesh_otimizada = mesh_processor.otimizar_para_venda(mesh)
    
    # 4. Exporta em MÚLTIPLOS formatos
    nome_base = os.path.splitext(os.path.basename(caminho_imagem))[0]
    
    # 4a. GLB (universal, com textura embutida) - MELHOR PARA VENDA
    caminho_glb = f"outputs/{nome_base}.glb"
    mesh_otimizada.export(caminho_glb)
    print(f"   ✅ GLB salvo: {caminho_glb}")
    
    # 4b. STL (padrão para impressão 3D)
    caminho_stl = f"outputs/{nome_base}.stl"
    mesh_otimizada.export(caminho_stl)
    print(f"   ✅ STL salvo: {caminho_stl}")
    
    # 4c. OBJ (para compatibilidade)
    caminho_obj = f"outputs/{nome_base}.obj"
    mesh_otimizada.export(caminho_obj)
    print(f"   ✅ OBJ salvo: {caminho_obj}")
    
    print(f"\n✅ Modelo gerado com sucesso em 3 formatos!")
    print("=" * 50)
    return mesh_otimizada

if __name__ == "__main__":
    # Cria pastas se não existirem
    os.makedirs("inputs", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    print("\n🎨 3dCreator - Conversor 2D para 3D")
    print("Coloque uma imagem na pasta 'inputs/' e execute novamente.")
    print("Exemplo: inputs/minha_foto.png\n")
    
    # Lista imagens disponíveis
    imagens = [f for f in os.listdir("inputs") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not imagens:
        print("❌ Nenhuma imagem encontrada na pasta 'inputs/'")
        print("   Coloque uma imagem e execute novamente.")
    else:
        print(f"📸 Imagens encontradas: {imagens}")
        for img in imagens:
            processar_imagem(f"inputs/{img}")