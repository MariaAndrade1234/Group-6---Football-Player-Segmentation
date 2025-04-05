import os
import imagehash
from PIL import Image
from collections import defaultdict
import pandas as pd
import json

# Caminhos
IMAGE_DIR = os.path.expanduser("~/Group-6---Football-Player-Segmentation/data/raw/images")
ANNOTATIONS_PATH = os.path.expanduser("~/Group-6---Football-Player-Segmentation/data/raw/annotations/instances_default.json")
OUTPUT_DIR = os.path.expanduser("~/Group-6---Football-Player-Segmentation/scripts/data/duplicates/reports")

# Garante que a pasta de saída exista
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_image_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)
    except Exception as e:
        print(f"Erro ao processar {image_path}: {e}")
        return None

def encontrar_imagens_duplicadas():
    print("🔍 Verificando imagens duplicadas...")
    hashes = defaultdict(list)
    duplicatas = []

    for filename in os.listdir(IMAGE_DIR):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(IMAGE_DIR, filename)
            img_hash = get_image_hash(path)
            if img_hash:
                if img_hash in hashes:
                    duplicatas.append((filename, hashes[img_hash][0]))
                hashes[img_hash].append(filename)

    print(f"\n✅ Duplicatas encontradas ({len(duplicatas)}):")
    for dup in duplicatas:
        print(f"- {dup[0]} é duplicata de {dup[1]}")

    return duplicatas, hashes

def verificar_duplicatas_metadados():
    print("\n📋 Verificando duplicações nos metadados...")
    with open(ANNOTATIONS_PATH, 'r') as f:
        data = json.load(f)

    image_ids = [img['id'] for img in data.get('images', [])]
    unique_ids = set(image_ids)
    duplicated_ids = [i for i in image_ids if image_ids.count(i) > 1]

    print(f"\n📌 Total de imagens: {len(image_ids)}")
    print(f"📌 IDs únicos: {len(unique_ids)}")
    print(f"🚨 IDs duplicados encontrados: {len(set(duplicated_ids))}")
    return image_ids, unique_ids, duplicated_ids

def gerar_relatorios(duplicatas, hashes, image_ids, unique_ids, duplicated_ids):
    print("\n📊 Quantificando impacto das duplicações:")

    total_imagens = len(os.listdir(IMAGE_DIR))
    total_duplicatas = len(duplicatas)
    total_unicas = len(set([item for sublist in hashes.values() for item in sublist])) - total_duplicatas
    percentual = (total_duplicatas / total_imagens) * 100 if total_imagens else 0

    print(f"- Total de imagens: {total_imagens}")
    print(f"- Imagens únicas: {total_unicas}")
    print(f"- Número de duplicatas: {total_duplicatas}")
    print(f"- Percentual de duplicação: {percentual:.2f}%")

    # Gerar CSV
    df_dup = pd.DataFrame(duplicatas, columns=["Arquivo_Duplicado", "Original"])
    df_dup.to_csv(os.path.join(OUTPUT_DIR, "duplicatas.csv"), index=False)

    df_unique = pd.DataFrame(list(set([img for sublist in hashes.values() for img in sublist if len(sublist) == 1])), columns=["Imagens_Únicas"])
    df_unique.to_csv(os.path.join(OUTPUT_DIR, "imagens_unicas.csv"), index=False)

    with open(os.path.join(OUTPUT_DIR, "relatorio_geral.txt"), "w") as f:
        f.write("RELATÓRIO DE DUPLICAÇÃO DE IMAGENS\n\n")
        f.write(f"Total de imagens: {total_imagens}\n")
        f.write(f"Imagens únicas: {total_unicas}\n")
        f.write(f"Número de duplicatas: {total_duplicatas}\n")
        f.write(f"Percentual de duplicação: {percentual:.2f}%\n")
        f.write(f"\nIDs de imagem no JSON: {len(image_ids)}")
        f.write(f"\nIDs únicos: {len(unique_ids)}")
        f.write(f"\nIDs duplicados: {len(set(duplicated_ids))}")

if __name__ == "__main__":
    duplicatas, hashes = encontrar_imagens_duplicadas()
    image_ids, unique_ids, duplicated_ids = verificar_duplicatas_metadados()
    gerar_relatorios(duplicatas, hashes, image_ids, unique_ids, duplicated_ids)





















