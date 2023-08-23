from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
import joblib
import numpy as np
import pandas as pd
import os

directory = os.path.join('train/')
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

features = ['sk_x_mean', 'sk_x_std', 'sk_x_mdn', 'sk_x_min', 'sk_x_max', 'sk_x_aad', 'sk_x_rms', 'sk_x_iqr', 'sk_x_skw', 'sk_x_krt', 'sk_x_var', 
            'sk_y_mean', 'sk_y_std', 'sk_y_mdn', 'sk_y_min', 'sk_y_max', 'sk_y_aad', 'sk_y_rms', 'sk_y_iqr', 'sk_y_skw', 'sk_y_krt', 'sk_y_var',
            'sk_z_mean', 'sk_z_std', 'sk_z_mdn', 'sk_z_min', 'sk_z_max', 'sk_z_aad', 'sk_z_rms', 'sk_z_iqr', 'sk_z_skw', 'sk_z_krt', 'sk_z_var',
            'th_x_mean', 'th_x_std', 'th_x_mdn', 'th_x_min', 'th_x_max', 'th_x_aad', 'th_x_rms', 'th_x_iqr', 'th_x_skw', 'th_x_krt', 'th_x_var',
            'th_y_mean', 'th_y_std', 'th_y_mdn', 'th_y_min', 'th_y_max', 'th_y_aad', 'th_y_rms', 'th_y_iqr', 'th_y_skw', 'th_y_krt', 'th_y_var',
            'th_z_mean', 'th_z_std', 'th_z_mdn', 'th_z_min', 'th_z_max', 'th_z_aad', 'th_z_rms', 'th_z_iqr', 'th_z_skw', 'th_z_krt', 'th_z_var',
            'tk_x_mean', 'tk_x_std', 'tk_x_mdn', 'tk_x_min', 'tk_x_max', 'tk_x_aad', 'tk_x_rms', 'tk_x_iqr', 'tk_x_skw', 'tk_x_krt', 'tk_x_var',
            'tk_y_mean', 'tk_y_std', 'tk_y_mdn', 'tk_y_min', 'tk_y_max', 'tk_y_aad', 'tk_y_rms', 'tk_y_iqr', 'tk_y_skw', 'tk_y_krt', 'tk_y_var',
            'tk_z_mean', 'tk_z_std', 'tk_z_mdn', 'tk_z_min', 'tk_z_max', 'tk_z_aad', 'tk_z_rms', 'tk_z_iqr', 'tk_z_skw', 'tk_z_krt', 'tk_z_var']

features_2 = [  'sk_mean', 'sk_std', 'sk_mdn', 'sk_min', 'sk_max', 'sk_aad', 'sk_rms', 'sk_iqr', 'sk_skw', 'sk_krt', 'sk_var',
                    'th_mean', 'th_std', 'th_mdn', 'th_min', 'th_max', 'th_aad', 'th_rms', 'th_iqr', 'th_skw', 'th_krt', 'th_var',
                    'tk_mean', 'tk_std', 'tk_mdn', 'tk_min', 'tk_max', 'tk_aad', 'tk_rms', 'tk_iqr', 'tk_skw', 'tk_krt', 'tk_var']

features_3 = ['mean', 'std', 'mdn', 'min', 'max', 'aad', 'rms', 'iqr', 'skw', 'krt', 'var']

all_features = features + features_2 + features_3

label = 'FoG'

X_train_complete = []
y_train_complete = []
for file in os.listdir(directory):
    if file.endswith(".csv"):
        #print(file)
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path, sep=',')
        """
        # Check for NaN values in the entire DataFrame
        nan_values = df.isna()
        # Check for NaN values in each column
        nan_counts = nan_values.sum()
        # Display the count of NaN values for each column
        print(nan_counts)
        print(f"Nan values in {file}: {nan_counts.sum()}")
        """
        X_train = np.array(df[all_features])
        y_train = np.array(df[label])
        X_train_complete.append(X_train)
        y_train_complete.append(y_train)

X_train = np.concatenate(X_train_complete)
y_train = np.concatenate(y_train_complete)

# Impute missing values
X_train = imputer.fit_transform(X_train)

# Initialize and train the Random Forest Classifier
# Initialize and train the Logistic Regression Classifier
lr_classifier = LogisticRegression(max_iter=10000, solver='saga', C=0.1)
lr_classifier.fit(X_train, y_train)

# Load the test file
print(os.listdir('test/'))
df = pd.read_csv('test/'+os.listdir('test/')[0], sep=',')
X_test = np.array(df[all_features])
y_test = np.array(df[label])

# Impute missing values
X_test = imputer.transform(X_test)

# Make predictions on the test set
y_pred = lr_classifier.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

# Save the model
joblib.dump(lr_classifier, 'lr_classifier.pkl')
