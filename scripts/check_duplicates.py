import os
import cv2
import numpy as np
from tqdm import tqdm
import hashlib
import json
from collections import defaultdict
from PIL import Image
from skimage.metrics import structural_similarity as ssim  # Importação do SSIM da skimage

def calculate_hash(image_path, hash_size=16):
    """Calcula hash perceptual para detecção de imagens similares"""
    try:
        # Usar PIL para abrir a imagem de forma mais robusta
        with Image.open(image_path) as img:
            img = img.convert("L").resize((hash_size, hash_size), Image.LANCZOS)
            pixels = np.array(img).flatten()
            avg = pixels.mean()
            bits = "".join(['1' if pixel > avg else '0' for pixel in pixels])
            hex_hash = "{0:0{1}x}".format(int(bits, 2), len(bits) // 4)
        return hex_hash
    except Exception as e:
        print(f"Erro ao processar {image_path}: {str(e)}")
        return None

def find_duplicates(images_dir, output_json="duplicates.json", threshold=0.95):
    """Encontra imagens duplicadas ou muito similares"""
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Analisando {len(image_files)} imagens para duplicatas...")
    
    # Estratégia 1: Hash de arquivo (duplicatas exatas)
    file_hashes = defaultdict(list)
    
    # Estratégia 2: Hash perceptual (imagens visualmente similares)
    perceptual_hashes = defaultdict(list)
    
    # Estratégia 3: Comparação estrutural (para maior precisão)
    duplicates = defaultdict(list)
    
    # Primeira passada: hashes rápidos
    for filename in tqdm(image_files, desc="Calculando hashes"):
        filepath = os.path.join(images_dir, filename)
        
        # Hash do arquivo (exato)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        file_hashes[file_hash].append(filename)
        
        # Hash perceptual
        phash = calculate_hash(filepath)
        if phash:
            perceptual_hashes[phash].append(filename)
    
    # Identificar possíveis duplicatas
    potential_duplicates = set()
    
    # Verificar duplicatas exatas
    for hash_val, files in file_hashes.items():
        if len(files) > 1:
            for f in files[1:]:
                potential_duplicates.add(f)
            duplicates[files[0]].extend(files[1:])
    
    # Verificar similares perceptuais
    for hash_val, files in perceptual_hashes.items():
        if len(files) > 1:
            # Comparação mais precisa entre os possíveis similares
            for i in range(len(files)):
                for j in range(i+1, len(files)):
                    img1 = cv2.imread(os.path.join(images_dir, files[i]))
                    img2 = cv2.imread(os.path.join(images_dir, files[j]))
                    
                    if img1 is None or img2 is None:
                        continue
                    
                    # Redimensionar para comparação
                    img1 = cv2.resize(img1, (256, 256))
                    img2 = cv2.resize(img2, (256, 256))
                    
                    # Converter para escala de cinza
                    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                    
                    # Calcular SSIM
                    score, _ = ssim(img1_gray, img2_gray, full=True)  # Usando o SSIM do skimage
                    
                    if score > threshold:
                        potential_duplicates.add(files[j])
                        duplicates[files[i]].append(files[j])
    
    # Salvar resultados
    with open(output_json, 'w') as f:
        json.dump(duplicates, f, indent=2)
    
    print(f"\nIdentificadas {len(potential_duplicates)} possíveis duplicatas.")
    print(f"Resultados salvos em {output_json}")
    
    return duplicates

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str, required=True, help='Diretório com imagens para verificar')
    parser.add_argument('--output_json', type=str, default="duplicates.json", help='Arquivo para salvar resultados')
    parser.add_argument('--threshold', type=float, default=0.95, help='Limite de similaridade (0-1)')
    args = parser.parse_args()
    
    os.makedirs(os.path.dirname(args.output_json) or '.', exist_ok=True)
    find_duplicates(args.images_dir, args.output_json, args.threshold)
import os
import hashlib
import cv2
import numpy as np
import json
from collections import defaultdict
from tqdm import tqdm
from PIL import Image
from skimage.metrics import structural_similarity as ssim

def calculate_hash(image_path, hash_size=16):
    """Calcula hash perceptual para detecção de imagens similares"""
    try:
        # Usar PIL para abrir a imagem de forma mais robusta
        with Image.open(image_path) as img:
            img = img.convert("L").resize((hash_size, hash_size), Image.LANCZOS)
            pixels = np.array(img).flatten()
            avg = pixels.mean()
            bits = "".join(['1' if pixel > avg else '0' for pixel in pixels])
            hex_hash = "{0:0{1}x}".format(int(bits, 2), len(bits) // 4)
        return hex_hash
    except Exception as e:
        print(f"Erro ao processar {image_path}: {str(e)}")
        return None

def find_duplicates(images_dir, output_json="duplicates.json", threshold=0.95):
    """Encontra duplicatas exatas e similares"""
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f"Analisando {len(image_files)} imagens para duplicatas...")
    
    # Estratégia 1: Hash de arquivo (duplicatas exatas)
    file_hashes = defaultdict(list)
    
    # Estratégia 2: Hash perceptual (imagens visualmente similares)
    perceptual_hashes = defaultdict(list)
    
    # Estratégia 3: Comparação estrutural (para maior precisão)
    duplicates = defaultdict(list)
    
    # Primeira passada: hashes rápidos
    for filename in tqdm(image_files, desc="Calculando hashes"):
        filepath = os.path.join(images_dir, filename)
        
        # Hash do arquivo (exato)
        with open(filepath, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        file_hashes[file_hash].append(filename)
        
        # Hash perceptual
        phash = calculate_hash(filepath)
        if phash:
            perceptual_hashes[phash].append(filename)
    
    # Identificar duplicatas exatas
    exact_duplicates = defaultdict(list)
    for hash_val, files in file_hashes.items():
        if len(files) > 1:
            for f in files[1:]:
                exact_duplicates[files[0]].append(f)
    
    # Identificar duplicatas perceptuais (visualmente semelhantes)
    potential_duplicates = defaultdict(list)
    for hash_val, files in perceptual_hashes.items():
        if len(files) > 1:
            # Comparação mais precisa entre os possíveis similares
            for i in range(len(files)):
                for j in range(i+1, len(files)):
                    img1 = cv2.imread(os.path.join(images_dir, files[i]))
                    img2 = cv2.imread(os.path.join(images_dir, files[j]))
                    
                    if img1 is None or img2 is None:
                        continue
                    
                    # Redimensionar para comparação
                    img1 = cv2.resize(img1, (256, 256))
                    img2 = cv2.resize(img2, (256, 256))
                    
                    # Converter para escala de cinza
                    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                    
                    # Calcular SSIM
                    score, _ = ssim(img1_gray, img2_gray, full=True)
                    
                    if score > threshold:
                        potential_duplicates[files[i]].append(files[j])
    
    # Salvar resultados
    results = {
        "exact_duplicates": exact_duplicates,
        "similar_duplicates": potential_duplicates
    }
    
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nIdentificadas {len(exact_duplicates)} duplicatas exatas e {len(potential_duplicates)} duplicatas semelhantes.")
    print(f"Resultados salvos em {output_json}")
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_dir', type=str, required=True, help='Diretório com imagens para verificar')
    parser.add_argument('--output_json', type=str, default="duplicates.json", help='Arquivo para salvar resultados')
    parser.add_argument('--threshold', type=float, default=0.95, help='Limite de similaridade (0-1) para duplicatas semelhantes')
    args = parser.parse_args()
    
    os.makedirs(os.path.dirname(args.output_json) or '.', exist_ok=True)
    find_duplicates(args.images_dir, args.output_json, args.threshold)
import os
import cv2
import json
import numpy as np
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm

def compare_images(image1_path, image2_path):
    # Carregar as imagens
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    if img1 is None or img2 is None:
        return None

    # Redimensionar as imagens para o mesmo tamanho
    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))

    # Converter para escala de cinza
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calcular o SSIM
    score, _ = ssim(img1_gray, img2_gray, full=True)
    return score

def find_duplicates(images_dir, threshold, output_json):
    # Obter todas as imagens no diretório
    files = [f for f in os.listdir(images_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    potential_duplicates = {}

    print(f"Analisando {len(files)} imagens para duplicatas...")

    # Comparar cada par de imagens
    for i in tqdm(range(len(files))):
        for j in range(i+1, len(files)):
            image1_path = os.path.join(images_dir, files[i])
            image2_path = os.path.join(images_dir, files[j])

            # Comparar as imagens
            score = compare_images(image1_path, image2_path)

            if score is not None:
                print(f"Comparando {files[i]} e {files[j]}: SSIM = {score}")  # Exibindo o valor de SSIM
                if score > threshold:
                    if files[i] not in potential_duplicates:
                        potential_duplicates[files[i]] = []
                    potential_duplicates[files[i]].append(files[j])

    # Salvar os resultados em um arquivo JSON
    with open(output_json, 'w') as json_file:
        json.dump(potential_duplicates, json_file, indent=4)

    print(f"Resultados salvos em {output_json}")
    return potential_duplicates

if __name__ == "__main__":
    images_dir = "/home/beatrizdev/grupo6/archive (1)/data/images"  # Diretório de imagens
    threshold = 0.85  # Limiar para detectar imagens semelhantes
    output_json = "resultados.json"  # Arquivo de saída para os resultados

    find_duplicates(images_dir, threshold, output_json)
