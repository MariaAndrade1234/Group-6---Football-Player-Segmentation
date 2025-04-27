import os
import shutil
import random

# Caminhos base
base_dir = "/home/beatrizdev/grupo6/archive (1)/data/images"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")

# Cria os diretórios se não existirem
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Lista apenas imagens válidas
all_images = [f for f in os.listdir(base_dir) if f.endswith(('.jpg', '.png')) and os.path.isfile(os.path.join(base_dir, f))]

# Embaralha
random.shuffle(all_images)

# Divide 80% treino, 20% validação
split_idx = int(len(all_images) * 0.8)
train_images = all_images[:split_idx]
val_images = all_images[split_idx:]

# Função para mover imagem e txt correspondente (se existir)
def move_pair(img_list, destination):
    for img_file in img_list:
        # Caminho da imagem
        src_img = os.path.join(base_dir, img_file)
        dst_img = os.path.join(destination, img_file)
        shutil.move(src_img, dst_img)

        # Caminho do txt correspondente
        txt_file = os.path.splitext(img_file)[0] + ".txt"
        src_txt = os.path.join(base_dir, txt_file)
        dst_txt = os.path.join(destination, txt_file)
        if os.path.exists(src_txt):
            shutil.move(src_txt, dst_txt)

# Move arquivos
move_pair(train_images, train_dir)
move_pair(val_images, val_dir)

print(f"Total imagens: {len(all_images)}")
print(f"Treino: {len(train_images)}")
print(f"Validação: {len(val_images)}")

