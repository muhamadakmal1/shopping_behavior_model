from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.cluster import KMeans
import pickle
import os

app = Flask(__name__)

# Global variables to store data and models
df = None
df_with_clusters = None
cluster_analysis = None
feature_importance = None
models = {}

def load_data():
    """Load all data files"""
    global df, df_with_clusters, cluster_analysis, feature_importance
    
    try:
        df = pd.read_csv('shopping_behavior_updated.csv')
        
        if os.path.exists('shopping_behavior_with_clusters.csv'):
            df_with_clusters = pd.read_csv('shopping_behavior_with_clusters.csv')
        
        if os.path.exists('cluster_analysis.csv'):
            cluster_analysis = pd.read_csv('cluster_analysis.csv')
        
        if os.path.exists('feature_importance.csv'):
            feature_importance = pd.read_csv('feature_importance.csv')
        
        return True
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def train_models():
    """Load ML models from disk"""
    global models
    
    try:
        # Try to load saved models
        from model_loader import load_models
        loaded_models = load_models()
        
        models['regression'] = loaded_models['regression']
        models['classification'] = loaded_models['classification']
        models['clustering'] = loaded_models['clustering']
        models['label_encoders'] = loaded_models['label_encoders']
        models['scaler'] = loaded_models['scaler']
        models['cluster_scaler'] = loaded_models['cluster_scaler']
        models['feature_columns'] = loaded_models['feature_columns']
        
        print("[OK] Models loaded from disk successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Please run 'python train_models.py' first to train and save the models.")
        return False


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/overview')
def get_overview():
    """Get dataset overview statistics"""
    stats = {
        'total_customers': len(df),
        'avg_purchase_amount': float(df['Purchase Amount (USD)'].mean()),
        'total_revenue': float(df['Purchase Amount (USD)'].sum()),
        'avg_age': float(df['Age'].mean()),
        'avg_rating': float(df['Review Rating'].mean()),
        'subscription_rate': float((df['Subscription Status'] == 'Yes').sum() / len(df) * 100),
        'discount_usage': float((df['Discount Applied'] == 'Yes').sum() / len(df) * 100),
        'male_percentage': float((df['Gender'] == 'Male').sum() / len(df) * 100),
        'female_percentage': float((df['Gender'] == 'Female').sum() / len(df) * 100)
    }
    return jsonify(stats)

@app.route('/api/purchase_by_category')
def purchase_by_category():
    """Get purchase statistics by category"""
    category_stats = df.groupby('Category').agg({
        'Purchase Amount (USD)': ['mean', 'sum', 'count']
    }).round(2)
    
    result = []
    for category in category_stats.index:
        result.append({
            'category': category,
            'avg_purchase': float(category_stats.loc[category, ('Purchase Amount (USD)', 'mean')]),
            'total_revenue': float(category_stats.loc[category, ('Purchase Amount (USD)', 'sum')]),
            'count': int(category_stats.loc[category, ('Purchase Amount (USD)', 'count')])
        })
    
    return jsonify(result)

@app.route('/api/age_distribution')
def age_distribution():
    """Get age distribution data"""
    age_bins = [18, 25, 35, 45, 55, 70]
    age_labels = ['18-24', '25-34', '35-44', '45-54', '55-70']
    
    df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)
    age_dist = df['Age_Group'].value_counts().sort_index()
    
    result = [{'age_group': str(group), 'count': int(count)} for group, count in age_dist.items()]
    return jsonify(result)

@app.route('/api/seasonal_trends')
def seasonal_trends():
    """Get seasonal purchase trends"""
    season_stats = df.groupby('Season').agg({
        'Purchase Amount (USD)': ['mean', 'sum', 'count']
    }).round(2)
    
    result = []
    for season in season_stats.index:
        result.append({
            'season': season,
            'avg_purchase': float(season_stats.loc[season, ('Purchase Amount (USD)', 'mean')]),
            'total_revenue': float(season_stats.loc[season, ('Purchase Amount (USD)', 'sum')]),
            'count': int(season_stats.loc[season, ('Purchase Amount (USD)', 'count')])
        })
    
    return jsonify(result)

@app.route('/api/top_items')
def top_items():
    """Get top selling items"""
    top_items = df['Item Purchased'].value_counts().head(10)
    result = [{'item': item, 'count': int(count)} for item, count in top_items.items()]
    return jsonify(result)

@app.route('/api/cluster_data')
def cluster_data():
    """Get cluster analysis data"""
    if df_with_clusters is not None and 'Cluster' in df_with_clusters.columns:
        cluster_stats = df_with_clusters.groupby('Cluster').agg({
            'Age': 'mean',
            'Purchase Amount (USD)': 'mean',
            'Previous Purchases': 'mean',
            'Review Rating': 'mean',
            'Customer ID': 'count'
        }).round(2)
        
        result = []
        for cluster in cluster_stats.index:
            result.append({
                'cluster': int(cluster),
                'avg_age': float(cluster_stats.loc[cluster, 'Age']),
                'avg_purchase': float(cluster_stats.loc[cluster, 'Purchase Amount (USD)']),
                'avg_prev_purchases': float(cluster_stats.loc[cluster, 'Previous Purchases']),
                'avg_rating': float(cluster_stats.loc[cluster, 'Review Rating']),
                'customer_count': int(cluster_stats.loc[cluster, 'Customer ID'])
            })
        
        return jsonify(result)
    
    return jsonify([])

@app.route('/api/feature_importance_data')
def feature_importance_data():
    """Get feature importance data"""
    if feature_importance is not None:
        result = feature_importance.head(10).to_dict('records')
        return jsonify(result)
    
    return jsonify([])

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make predictions based on user input"""
    try:
        data = request.json
        
        # Prepare features
        features = {
            'Age': data.get('age', 30),
            'Previous Purchases': data.get('previous_purchases', 10),
            'Review Rating': data.get('review_rating', 3.5),
            'Is_Subscriber': 1 if data.get('is_subscriber', False) else 0,
            'Discount_Used': 1 if data.get('discount_used', False) else 0,
            'Promo_Used': 1 if data.get('promo_used', False) else 0
        }
        
        # Encode categorical features
        le_dict = models['label_encoders']
        
        features['Gender_encoded'] = le_dict['Gender'].transform([data.get('gender', 'Male')])[0]
        features['Category_encoded'] = le_dict['Category'].transform([data.get('category', 'Clothing')])[0]
        features['Season_encoded'] = le_dict['Season'].transform([data.get('season', 'Spring')])[0]
        features['Frequency of Purchases_encoded'] = le_dict['Frequency of Purchases'].transform([data.get('frequency', 'Weekly')])[0]
        
        # Create feature array
        feature_array = np.array([[features[col] for col in models['feature_columns']]])
        
        # Make predictions
        purchase_prediction = float(models['regression'].predict(feature_array)[0])
        subscription_prob = float(models['classification'].predict_proba(feature_array)[0][1])
        
        result = {
            'predicted_purchase_amount': round(purchase_prediction, 2),
            'subscription_probability': round(subscription_prob * 100, 2)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/payment_methods')
def payment_methods():
    """Get payment method distribution"""
    payment_dist = df['Payment Method'].value_counts()
    result = [{'method': method, 'count': int(count)} for method, count in payment_dist.items()]
    return jsonify(result)

@app.route('/api/recent_transactions')
def recent_transactions():
    """Get recent transactions"""
    recent = df.head(50)[['Customer ID', 'Age', 'Gender', 'Item Purchased', 'Category', 
                          'Purchase Amount (USD)', 'Review Rating', 'Subscription Status']].to_dict('records')
    return jsonify(recent)

if __name__ == '__main__':
    print("Loading data...")
    if load_data():
        print("Training models...")
        train_models()
        print("\nStarting Flask server...")
        print("Open http://127.0.0.1:5000 in your browser")
        app.run(debug=True, port=5000)
    else:
        print("Failed to load data. Please check if CSV files exist.")
