from ultralytics import YOLO
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from PIL import Image
import numpy as np

def evaluate_model(model_path, data_yaml, split='val', conf=0.5):
    """
    Evaluate trained YOLOv8 model
    
    Args:
        model_path (str): Path to trained model
        data_yaml (str): Path to data.yaml
        split (str): Dataset split to evaluate ('val' or 'test')
        conf (float): Confidence threshold
    """
    # Load model
    model = YOLO(model_path)
    
    # Evaluate
    metrics = model.val(data=data_yaml, split=split, conf=conf)
    print(f"mAP50-95: {metrics.box.map:.2f}")
    print(f"mAP50: {metrics.box.map50:.2f}")
    
    # Plot confusion matrix
    conf_matrix = metrics.confusion_matrix.matrix
    classes = list(metrics.names.values())
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', 
                xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(os.path.join('results', 'visualizations', 'confusion_matrix.png'))
    plt.close()
    
    # Save metrics
    metrics_df = pd.DataFrame({
        'mAP50': [metrics.box.map50],
        'mAP50-95': [metrics.box.map],
        'precision': [metrics.box.mp],
        'recall': [metrics.box.mr]
    })
    metrics_df.to_csv(os.path.join('results', 'metrics', 'model_metrics.csv'), index=False)
    
    return metrics

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, required=True, help='Path to trained model')
    parser.add_argument('--data_yaml', type=str, required=True, help='Path to data.yaml')
    parser.add_argument('--split', type=str, default='val', help='Dataset split to evaluate')
    parser.add_argument('--conf', type=float, default=0.5, help='Confidence threshold')
    args = parser.parse_args()
    
    os.makedirs('results/metrics', exist_ok=True)
    os.makedirs('results/visualizations', exist_ok=True)
    
    evaluate_model(args.model_path, args.data_yaml, args.split, args.conf)