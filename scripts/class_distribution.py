import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import pandas as pd

# Caminho para o arquivo de anotações COCO
annotations_path = 'C:/Users/pblvv/OneDrive/Documentos/Machine Learning Avanti/archive/annotations/instances_default.json'
images_path = 'C:/Users/pblvv/OneDrive/Documentos/Machine Learning Avanti/archive/images/'

# Carregar as anotações COCO
coco = COCO(annotations_path)

# Mapas auxiliares
categories = coco.loadCats(coco.getCatIds())
id_to_name = {cat['id']: cat['name'] for cat in categories}
id_to_filename = {img['id']: img['file_name'] for img in coco.loadImgs(coco.getImgIds())}

# Construir DataFrame com info das anotações
data = []
for ann in coco.dataset['annotations']:
    data.append({
        'image_id': ann['image_id'],
        'file_name': id_to_filename[ann['image_id']],
        'category_id': ann['category_id'],
        'category_name': id_to_name[ann['category_id']],
        'area': ann['area'],
        'bbox': ann['bbox'],
        'iscrowd': ann['iscrowd'],
        'segmentation': ann['segmentation'],
    })

df = pd.DataFrame(data)

# Contagem por classe
annotation_counts = df['category_name'].value_counts()
image_counts_per_class = df.groupby('category_name')['image_id'].nunique()

# Print de distribuição
print("Distribuição das classes:")
for category in annotation_counts.index:
    print(f"- Classe '{category}': {annotation_counts[category]} anotações, presentes em {image_counts_per_class[category]} imagens")

# Exibir as classes e a quantidade de imagens por classe
print("\nClasses existentes e número de imagens por classe:")
for category, image_count in image_counts_per_class.items():
    print(f"- Classe '{category}' tem {image_count} imagens.")

# Verificar desequilíbrio
max_count = annotation_counts.max()
min_count = annotation_counts.min()
desequilibrado = (max_count / min_count) > 1.5

print("\nDesequilíbrio identificado?", "Sim" if desequilibrado else "Não")
if desequilibrado:
    majoritaria = annotation_counts.idxmax()
    minoritaria = annotation_counts.idxmin()
    print(f"A classe mais frequente ({majoritaria}) tem {max_count} anotações.")
    print(f"A menos frequente ({minoritaria}) tem {min_count} anotações.")

# Visualizar a distribuição
plt.figure(figsize=(10, 5))
plt.bar(annotation_counts.index, annotation_counts.values, color='skyblue')
plt.title("Distribuição das Classes no Dataset")
plt.xlabel("Classe")
plt.ylabel("Número de Anotações")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()