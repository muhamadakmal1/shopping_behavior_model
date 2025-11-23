"""
Train and save machine learning models for shopping behavior prediction
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_report

print("="*80)
print("TRAINING MACHINE LEARNING MODELS")
print("="*80)

# Load data
print("\n1. Loading data...")
df = pd.read_csv('shopping_behavior_updated.csv')
print(f"   [OK] Loaded {len(df)} records")

# Prepare features
print("\n2. Preparing features...")
df_model = df.copy()
df_model['Is_Subscriber'] = (df_model['Subscription Status'] == 'Yes').astype(int)
df_model['Discount_Used'] = (df_model['Discount Applied'] == 'Yes').astype(int)
df_model['Promo_Used'] = (df_model['Promo Code Used'] == 'Yes').astype(int)

# Feature list
feature_cols = ['Age', 'Previous Purchases', 'Review Rating', 'Is_Subscriber', 'Discount_Used', 'Promo_Used']

# Encode categorical features
print("   - Encoding categorical features...")
le_dict = {}
categorical_features = ['Gender', 'Category', 'Season', 'Frequency of Purchases']

for col in categorical_features:
    le = LabelEncoder()
    df_model[f'{col}_encoded'] = le.fit_transform(df_model[col])
    le_dict[col] = le
    feature_cols.append(f'{col}_encoded')
    print(f"     [OK] Encoded {col}: {len(le.classes_)} classes")

# Prepare X and y
X = df_model[feature_cols]
y_regression = df_model['Purchase Amount (USD)']
y_classification = df_model['Is_Subscriber']

print(f"\n   [OK] Total features: {len(feature_cols)}")

# Split data
print("\n3. Splitting data (80%% train, 20%% test)...")
X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X, y_regression, test_size=0.2, random_state=42
)
_, _, y_train_clf, y_test_clf = train_test_split(
    X, y_classification, test_size=0.2, random_state=42
)
print(f"   [OK] Training set: {X_train.shape[0]} samples")
print(f"   [OK] Test set: {X_test.shape[0]} samples")

# Scale features
print("\n4. Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("   [OK] Features scaled using StandardScaler")

# MODEL 1: REGRESSION
print("\n5. Training Regression Model (Purchase Amount Prediction)...")
rf_regressor = RandomForestRegressor(
    n_estimators=100, random_state=42, max_depth=10,
    min_samples_split=5, min_samples_leaf=2
)
rf_regressor.fit(X_train_scaled, y_train_reg)

y_pred_reg = rf_regressor.predict(X_test_scaled)
mse = mean_squared_error(y_test_reg, y_pred_reg)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_reg, y_pred_reg)

print(f"   [OK] Model trained successfully!")
print(f"   [STAT] RMSE: ${rmse:.2f}")
print(f"   [STAT] R2 Score: {r2:.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf_regressor.feature_importances_
}).sort_values('importance', ascending=False)

# MODEL 2: CLASSIFICATION
print("\n6. Training Classification Model (Subscription Prediction)...")
rf_classifier = RandomForestClassifier(
    n_estimators=100, random_state=42, max_depth=10,
    min_samples_split=5, min_samples_leaf=2
)
rf_classifier.fit(X_train_scaled, y_train_clf)

y_pred_clf = rf_classifier.predict(X_test_scaled)
accuracy = (y_pred_clf == y_test_clf).sum() / len(y_test_clf)

print(f"   [OK] Model trained successfully!")
print(f"   [STAT] Accuracy: {accuracy*100:.2f}%%")

# MODEL 3: CLUSTERING
print("\n7. Training Clustering Model (Customer Segmentation)...")
clustering_features = ['Age', 'Purchase Amount (USD)', 'Previous Purchases', 'Review Rating']
X_cluster = df_model[clustering_features].copy()

scaler_cluster = StandardScaler()
X_cluster_scaled = scaler_cluster.fit_transform(X_cluster)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_cluster_scaled)

print(f"   [OK] Model trained successfully!")
print(f"   [STAT] Number of clusters: 4")

# SAVE MODELS
print("\n8. Saving models to disk...")
os.makedirs('models', exist_ok=True)

models_to_save = {
    'regression_model.pkl': rf_regressor,
    'classification_model.pkl': rf_classifier,
    'clustering_model.pkl': kmeans,
    'scaler.pkl': scaler,
    'cluster_scaler.pkl': scaler_cluster,
    'label_encoders.pkl': le_dict,
    'feature_columns.pkl': feature_cols,
    'feature_importance.pkl': feature_importance
}

for filename, model in models_to_save.items():
    filepath = os.path.join('models', filename)
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"   [OK] Saved: {filename}")

# Save metadata
metadata = {
    'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_samples': len(df),
    'n_features': len(feature_cols),
    'regression_rmse': rmse,
    'regression_r2': r2,
    'classification_accuracy': accuracy,
    'n_clusters': 4,
    'feature_names': feature_cols
}

with open('models/model_metadata.pkl', 'wb') as f:
    pickle.dump(metadata, f)
print(f"   [OK] Saved: model_metadata.pkl")

feature_importance.to_csv('feature_importance.csv', index=False)
print(f"   [OK] Saved: feature_importance.csv")

# SUMMARY
print("\n" + "="*80)
print("SUCCESS! MODEL TRAINING COMPLETE!")
print("="*80)
print(f"\nModels saved in: ./models/")
print(f"\nModel Performance Summary:")
print(f"   - Regression: RMSE=${rmse:.2f}, R2={r2:.4f}")
print(f"   - Classification: Accuracy={accuracy*100:.2f}%%")
print(f"   - Clustering: 4 segments, {len(df)} customers")
print("\nModels are ready for the Flask application!")
print("="*80)
