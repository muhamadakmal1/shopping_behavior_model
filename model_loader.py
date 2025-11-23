"""
Model loader utility for Flask application
"""
import pickle
import os

def load_models():
    """Load all trained models from disk"""
    models = {}
    model_dir = 'models'
    
    print("Loading models from disk...")
    
    # Load all pickle files
    model_files = {
        'regression': 'regression_model.pkl',
        'classification': 'classification_model.pkl',
        'clustering': 'clustering_model.pkl',
        'scaler': 'scaler.pkl',
        'cluster_scaler': 'cluster_scaler.pkl',
        'label_encoders': 'label_encoders.pkl',
        'feature_columns': 'feature_columns.pkl',
        'feature_importance': 'feature_importance.pkl',
        'metadata': 'model_metadata.pkl'
    }
    
    for key, filename in model_files.items():
        filepath = os.path.join(model_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                models[key] = pickle.load(f)
            print(f"  [OK] Loaded: {filename}")
        else:
            print(f"  [WARNING] Not found: {filename}")
    
    print(f"Models loaded successfully!\n")
    
    # Print model info
    if 'metadata' in models:
        meta = models['metadata']
        print("Model Information:")
        print(f"  Training Date: {meta['training_date']}")
        print(f"  Total Samples: {meta['total_samples']}")
        print(f"  Features: {meta['n_features']}")
        print(f"  Regression RMSE: ${meta['regression_rmse']:.2f}")
        print(f"  Regression R2: {meta['regression_r2']:.4f}")
        print(f"  Classification Accuracy: {meta['classification_accuracy']*100:.2f}%")
        print(f"  Clusters: {meta['n_clusters']}\n")
    
    return models

def get_model_info():
    """Get model metadata"""
    filepath = os.path.join('models', 'model_metadata.pkl')
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    return None
