import os
from PIL import Image

# --- Configurações ---
source_directory = "notebooks/outputs"
output_directory = "docs/figures_for_submission"
image_filenames = [
    "figura1_distribuicao_cafeina_total.png",
    "figura2_cafeina_por_nivel_H1.png",
    "figura3_cafeina_vs_horas_jogo_idade.png",
    "figura_ad_idade_vs_mg_cafeina_dia.png",
    "figura_ad_idade_vs_horas_jogo_principal_media_dia.png"
]
target_format = "JPEG"
target_dpi = (300, 300)
# --- Fim das Configurações ---

def convert_images():
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Diretório criado: {output_directory}")

    for filename in image_filenames:
        source_path = os.path.join(source_directory, filename)
        output_filename = os.path.splitext(filename)[0] + "." + target_format.lower()
        output_path = os.path.join(output_directory, output_filename)

        if not os.path.exists(source_path):
            print(f"Erro: Arquivo de origem não encontrado - {source_path}")
            continue

        try:
            img = Image.open(source_path)

            if img.mode == 'RGBA' or img.mode == 'P':
                img = img.convert('RGB')
            
            img.save(output_path, format=target_format, dpi=target_dpi, quality=95)
            print(f"Convertido: {filename} -> {output_filename} (DPI: {target_dpi[0]}) marginalised ")

        except Exception as e:
            print(f"Erro ao converter {filename}: {e}")

if __name__ == "__main__":
    print("Iniciando conversão de imagens...")
    try:
        from PIL import Image
    except ImportError:
        print("ERRO: A biblioteca Pillow não está instalada.")
        print("Por favor, instale-a executando: pip install Pillow")
        exit()
    
    convert_images()
    print("Conversão de imagens concluída.") 