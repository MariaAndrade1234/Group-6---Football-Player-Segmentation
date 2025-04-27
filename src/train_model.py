from ultralytics import YOLO
import yaml
import os

def train_yolov8(data_yaml, model_size='m', epochs=100, imgsz=640, batch=16):
    """
    Train YOLOv8 model for object detection
    
    Args:
        data_yaml (str): Path to YAML file with dataset configuration
        model_size (str): Model size (n, s, m, l, x)
        epochs (int): Number of training epochs
        imgsz (int): Image size
        batch (int): Batch size
    """
    # Load model
    model = YOLO(f'yolov8{model_size}.pt')
    
    # Train
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        name=f'football_yolov8{model_size}',
        save=True,
        save_period=10,
        val=True
    )
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_yaml', type=str, required=True, help='Path to data.yaml')
    parser.add_argument('--model_size', type=str, default='m', help='Model size (n,s,m,l,x)')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--imgsz', type=int, default=640, help='Image size')
    parser.add_argument('--batch', type=int, default=16, help='Batch size')
    args = parser.parse_args()
    
    # Create data.yaml if it doesn't exist
    if not os.path.exists(args.data_yaml):
        dataset_dir = os.path.abspath(os.path.join(os.path.dirname(args.data_yaml)))
        classes_path = os.path.join(dataset_dir, 'classes.txt')
        
        if not os.path.exists(classes_path):
            raise FileNotFoundError(f"'classes.txt' não encontrado em {classes_path}")
        
        # Read class names
        with open(classes_path, 'r') as f:
            class_names = [name.strip() for name in f.readlines() if name.strip()]
        
        # Create YAML content
        yaml_content = {
            'path': dataset_dir,
            'train': 'images/train',
            'val': 'images/val',
            'names': {i: name for i, name in enumerate(class_names)}
        }

        # Write to file
        with open(args.data_yaml, 'w') as f:
            yaml.dump(yaml_content, f, default_flow_style=False)
        print(f"Arquivo {args.data_yaml} criado com sucesso!")

    # Train the model
    train_yolov8(args.data_yaml, args.model_size, args.epochs, args.imgsz, args.batch)
