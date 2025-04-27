import os
import json
import shutil

# Caminho para o JSON com os resultados das duplicatas
json_path = "resultados.json"
# Caminho para a pasta com as imagens
images_dir = os.path.abspath("../data/images")
# Pasta de destino para as duplicatas
backup_dir = os.path.join(images_dir, "duplicatas_backup")

# Cria a pasta de backup, se ainda não existir
os.makedirs(backup_dir, exist_ok=True)

# Lê o JSON
with open(json_path, "r") as f:
    duplicatas = json.load(f)

# Contador para estatísticas
movidas = 0

for original, similares in duplicatas.items():
    for imagem in similares:
        origem = os.path.join(images_dir, imagem)
        destino = os.path.join(backup_dir, imagem)

        if os.path.exists(origem):
            shutil.move(origem, destino)
            print(f"Movido para backup: {imagem}")
            movidas += 1
        else:
            print(f"Arquivo não encontrado: {imagem}")

print(f"\nTotal de imagens movidas para backup: {movidas}")
