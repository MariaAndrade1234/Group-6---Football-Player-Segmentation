import os
import cv2
import xml.etree.ElementTree as ET

# Caminho das imagens e labels
data_path = '/home/beatrizdev/grupo6/archive (1)/data/'

# Caminho das imagens
images_path = os.path.join(data_path, 'images')

# Caminho de destino dos labels
labels_path = os.path.join(data_path, 'labels')

# Criar pasta de labels caso não exista
os.makedirs(labels_path, exist_ok=True)

# Função para converter XML para o formato YOLO
def xml_to_yolo(xml_file, image_width, image_height):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    labels = []
    for member in root.findall('object'):
        class_name = member.find('name').text
        class_id = 0  # Alterar para o ID da classe, se necessário
        bndbox = member.find('bndbox')
        
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        
        # Normalizar para o formato YOLO
        x_center = (xmin + xmax) / 2 / image_width
        y_center = (ymin + ymax) / 2 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height
        
        labels.append(f'{class_id} {x_center} {y_center} {width} {height}')
    
    return labels

# Processar imagens e converter XMLs para o formato YOLO
for image_file in os.listdir(images_path):
    if image_file.endswith('.jpg') or image_file.endswith('.png'):  # ou qualquer outra extensão de imagem
        image_path = os.path.join(images_path, image_file)
        
        # Obter o tamanho da imagem
        image = cv2.imread(image_path)
        image_height, image_width, _ = image.shape
        
        # Localizar o arquivo XML correspondente
        xml_file = os.path.splitext(image_file)[0] + '.xml'
        xml_path = os.path.join(data_path, 'annotations', xml_file)
        
        if os.path.exists(xml_path):
            labels = xml_to_yolo(xml_path, image_width, image_height)
            
            # Escrever o arquivo de label
            label_file = os.path.join(labels_path, os.path.splitext(image_file)[0] + '.txt')
            with open(label_file, 'w') as f:
                f.write('\n'.join(labels))

print("Conversão completa!")
