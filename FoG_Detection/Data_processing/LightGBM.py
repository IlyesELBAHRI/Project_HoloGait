import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import GridSearchCV

import os

directory = os.path.join('train/')
# Define your data
features = ['Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z', 'Shank_mean', 'Thigh_mean', 'Trunk_mean', 'MEAN']
label = 'FoG'


# Define the parameter grid for the grid search
param_grid = {
    'num_leaves': [1000, 5000, 9000, 12000],  # Example hyperparameter values to search
    'learning_rate': [0.1, 0.05, 0.01],
}

params = {
    'objective': 'binary',
    'boosting': 'goss', # gbdt, rf, dart, goss
    'learning_rate': 0.1,
    'num_leaves': 10000,
    'verbose': 0,
    'tree_learner': 'data'
    #'weight_column': weights
}

X_train_complete = []
y_train_complete = []

for file in os.listdir(directory):
    if file.endswith(".csv"):
        print(file)
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path, sep=',')
        X_train = np.array(df[features])
        y_train = np.array(df[label])
        X_train_complete.append(X_train)
        y_train_complete.append(y_train)

X_train = np.concatenate(X_train_complete)
y_train = np.concatenate(y_train_complete)


lgb_train = lgb.Dataset(X_train, y_train)
"""
model = lgb.LGBMClassifier()

# Perform grid search using cross-validation
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='balanced_accuracy')
grid_search.fit(X_train, y_train)
# Print the best parameters and score
print("Best Parameters:", grid_search.best_params_)
print("Best Balanced Accuracy:", grid_search.best_score_)
"""
# Train the model
model = lgb.train(params, lgb_train)

# Cross validation
#cv_results = lgb.cv(params, lgb_train, num_boost_round=100, nfold=10, metrics='binary_logloss', seed=42)
#print(cv_results)

# Save the trained model
model.save_model('trained_model.txt')

print("Training completed and model saved.")
