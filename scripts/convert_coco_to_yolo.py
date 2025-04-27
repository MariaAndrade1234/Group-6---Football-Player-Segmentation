import json
import os
import cv2
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import shutil

def convert_coco_to_yolo(coco_json_path, images_dir, output_dir):
    # Create output directories
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    
    # Load COCO JSON
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Create mappings
    id_to_img = {img['id']: img for img in coco_data['images']}
    id_to_ann = {img['id']: [] for img in coco_data['images']}
    for ann in coco_data['annotations']:
        id_to_ann[ann['image_id']].append(ann)
    
    # Get category mapping
    cat_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}
    cat_name_to_id = {cat['name']: i for i, cat in enumerate(coco_data['categories'])}
    
    # Split dataset
    img_ids = list(id_to_img.keys())
    train_ids, val_ids = train_test_split(img_ids, test_size=0.2, random_state=42)
    
    # Process images
    for split, ids in [('train', train_ids), ('val', val_ids)]:
        for img_id in tqdm(ids, desc=f'Processing {split} images'):
            img_info = id_to_img[img_id]
            img_path = os.path.join(images_dir, img_info['file_name'])
            img = cv2.imread(img_path)
            if img is None:
                continue
                
            h, w = img.shape[:2]
            
            # Prepare YOLO annotations
            yolo_lines = []
            for ann in id_to_ann[img_id]:
                cat_name = cat_id_to_name[ann['category_id']]
                cat_id = cat_name_to_id[cat_name]
                
                # COCO bbox format: [x_min, y_min, width, height]
                x, y, bw, bh = ann['bbox']
                
                # Convert to YOLO format: [x_center, y_center, width, height] (normalized)
                x_center = (x + bw / 2) / w
                y_center = (y + bh / 2) / h
                bw /= w
                bh /= h
                
                yolo_lines.append(f"{cat_id} {x_center} {y_center} {bw} {bh}\n")
            
            # Save YOLO annotations
            txt_name = os.path.splitext(img_info['file_name'])[0] + '.txt'
            txt_path = os.path.join(output_dir, 'labels', split, txt_name)
            with open(txt_path, 'w') as f:
                f.writelines(yolo_lines)
            
            # Copy image
            dest_img_path = os.path.join(output_dir, 'images', split, img_info['file_name'])
            shutil.copy(img_path, dest_img_path)
    
    # Save class names
    with open(os.path.join(output_dir, 'classes.txt'), 'w') as f:
        for cat_name in cat_name_to_id.keys():
            f.write(f"{cat_name}\n")
    
    print("Conversion completed successfully!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--coco_json', type=str, required=True, help='Path to COCO JSON file')
    parser.add_argument('--images_dir', type=str, required=True, help='Path to images directory')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory for YOLO format')
    args = parser.parse_args()
    
    convert_coco_to_yolo(args.coco_json, args.images_dir, args.output_dir)