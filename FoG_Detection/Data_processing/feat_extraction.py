import pandas as pd
import numpy as np
import os
import scipy.signal as signal
import scipy.fftpack as fft

from sklearn.preprocessing import StandardScaler



WINDOW = 150
STEP_SIZE = 75

#lecture des fichiers txt

directory = os.path.join('daphnet_csv/')
out_dir = "daphnet_windowed/"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

sampling_rate = 64 #Hz
frequency_range = (0.1, 8)
fft_frequencies = fft.rfftfreq(WINDOW, d=1.0/sampling_rate)




# Preprocess the feature data
scaler = StandardScaler()

features = ['Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z']
timestep = ['Timestep']

new_features = ['sk_x_mean', 'sk_x_std', 'sk_x_mdn', 'sk_x_min', 'sk_x_max', 'sk_x_aad', 'sk_x_rms', 'sk_x_iqr', 'sk_x_skw', 'sk_x_krt', 'sk_x_var', 
                'sk_y_mean', 'sk_y_std', 'sk_y_mdn', 'sk_y_min', 'sk_y_max', 'sk_y_aad', 'sk_y_rms', 'sk_y_iqr', 'sk_y_skw', 'sk_y_krt', 'sk_y_var',
                'sk_z_mean', 'sk_z_std', 'sk_z_mdn', 'sk_z_min', 'sk_z_max', 'sk_z_aad', 'sk_z_rms', 'sk_z_iqr', 'sk_z_skw', 'sk_z_krt', 'sk_z_var',
                'th_x_mean', 'th_x_std', 'th_x_mdn', 'th_x_min', 'th_x_max', 'th_x_aad', 'th_x_rms', 'th_x_iqr', 'th_x_skw', 'th_x_krt', 'th_x_var',
                'th_y_mean', 'th_y_std', 'th_y_mdn', 'th_y_min', 'th_y_max', 'th_y_aad', 'th_y_rms', 'th_y_iqr', 'th_y_skw', 'th_y_krt', 'th_y_var',
                'th_z_mean', 'th_z_std', 'th_z_mdn', 'th_z_min', 'th_z_max', 'th_z_aad', 'th_z_rms', 'th_z_iqr', 'th_z_skw', 'th_z_krt', 'th_z_var',
                'tk_x_mean', 'tk_x_std', 'tk_x_mdn', 'tk_x_min', 'tk_x_max', 'tk_x_aad', 'tk_x_rms', 'tk_x_iqr', 'tk_x_skw', 'tk_x_krt', 'tk_x_var',
                'tk_y_mean', 'tk_y_std', 'tk_y_mdn', 'tk_y_min', 'tk_y_max', 'tk_y_aad', 'tk_y_rms', 'tk_y_iqr', 'tk_y_skw', 'tk_y_krt', 'tk_y_var',
                'tk_z_mean', 'tk_z_std', 'tk_z_mdn', 'tk_z_min', 'tk_z_max', 'tk_z_aad', 'tk_z_rms', 'tk_z_iqr', 'tk_z_skw', 'tk_z_krt', 'tk_z_var']


new_features_2 = [  'sk_mean', 'sk_std', 'sk_mdn', 'sk_min', 'sk_max', 'sk_aad', 'sk_rms', 'sk_iqr', 'sk_skw', 'sk_krt', 'sk_var',
                    'th_mean', 'th_std', 'th_mdn', 'th_min', 'th_max', 'th_aad', 'th_rms', 'th_iqr', 'th_skw', 'th_krt', 'th_var',
                    'tk_mean', 'tk_std', 'tk_mdn', 'tk_min', 'tk_max', 'tk_aad', 'tk_rms', 'tk_iqr', 'tk_skw', 'tk_krt', 'tk_var']

new_features_3 = ['mean', 'std', 'mdn', 'min', 'max', 'aad', 'rms', 'iqr', 'skw', 'krt', 'var']

new_fft_features = ['fft_sk_mean', 'fft_sk_std', 'fft_sk_mdn', 'fft_sk_min', 'fft_sk_max', 'fft_sk_aad', 'fft_sk_rms', 'fft_sk_iqr', 'fft_sk_skw', 'fft_sk_krt', 'fft_sk_var',
                'fft_th_mean', 'fft_th_std', 'fft_th_mdn', 'fft_th_min', 'fft_th_max', 'fft_th_aad', 'fft_th_rms', 'fft_th_iqr', 'fft_th_skw', 'fft_th_krt', 'fft_th_var',
                'fft_tk_mean', 'fft_tk_std', 'fft_tk_mdn', 'fft_tk_min', 'fft_tk_max', 'fft_tk_aad', 'fft_tk_rms', 'fft_tk_iqr', 'fft_tk_skw', 'fft_tk_krt', 'fft_tk_var']

new_fft_features_2 = ['fft_mean', 'fft_std', 'fft_mdn', 'fft_min', 'fft_max', 'fft_aad', 'fft_rms', 'fft_iqr', 'fft_skw', 'fft_krt', 'fft_var']
label = ['FoG']

all_features = new_features + new_features_2 + new_features_3 + new_fft_features + new_fft_features_2


def extract_features(X):
    feat = []
    #mean
    feat.append(np.mean(X))
    #standard deviation
    feat.append(np.std(X))
    #median
    feat.append(np.median(X))
    #min
    feat.append(np.min(X))
    #max
    feat.append(np.max(X))
    #average absolute deviation
    feat.append(np.mean(np.absolute(X - np.mean(X))))
    #root mean square
    feat.append(np.sqrt(np.mean(np.square(X))))
    #interquartile range
    feat.append(np.percentile(X, 75) - np.percentile(X, 25))
    #skewness
    feat.append(np.mean(np.power((X - np.mean(X)) / np.std(X), 3))) if np.std(X) != 0 else feat.append(0)
    #kurtosis
    feat.append(np.mean(np.power((X - np.mean(X)) / np.std(X), 4))) if np.std(X) != 0 else feat.append(0)
    #variance
    feat.append(np.var(X))
    return feat




for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        print(filename)
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path, sep=',')
        new_df = pd.DataFrame(columns = timestep + all_features + label)
        k=0
        while k < len(df)-WINDOW:
            print(f"{k}/{len(df)} points processed\r", end="", flush=True)
            sk_x = df['Shank_x'][k:k+WINDOW]
            sk_y = df['Shank_y'][k:k+WINDOW]
            sk_z = df['Shank_z'][k:k+WINDOW]
            th_x = df['Thigh_x'][k:k+WINDOW]
            th_y = df['Thigh_y'][k:k+WINDOW]
            th_z = df['Thigh_z'][k:k+WINDOW]
            tk_x = df['Trunk_x'][k:k+WINDOW]
            tk_y = df['Trunk_y'][k:k+WINDOW]
            tk_z = df['Trunk_z'][k:k+WINDOW]

            sk_xyz = np.sqrt(np.square(sk_x) + np.square(sk_y) + np.square(sk_z))
            fft_sk_xyz = fft.rfft(sk_xyz.to_numpy())
            fft_sk_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0

            th_xyz = np.sqrt(np.square(th_x) + np.square(th_y) + np.square(th_z))
            fft_th_xyz = fft.rfft(th_xyz.to_numpy())
            fft_th_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0

            tk_xyz = np.sqrt(np.square(tk_x) + np.square(tk_y) + np.square(tk_z))
            fft_tk_xyz = fft.rfft(tk_xyz.to_numpy())
            fft_tk_xyz[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0

            all_imu = np.sqrt(np.square(sk_x) + np.square(sk_y) + np.square(sk_z) + np.square(th_x) + np.square(th_y) + np.square(th_z) + np.square(tk_x) + np.square(tk_y) + np.square(tk_z))
            fft_all_imu = fft.rfft(all_imu.to_numpy())
            fft_all_imu[(fft_frequencies < frequency_range[0]) | (fft_frequencies > frequency_range[1])] = 0
            
            features_1 = []
            features_1.extend(extract_features(sk_x))
            features_1.extend(extract_features(sk_y))
            features_1.extend(extract_features(sk_z))
            features_1.extend(extract_features(th_x))
            features_1.extend(extract_features(th_y))
            features_1.extend(extract_features(th_z))
            features_1.extend(extract_features(tk_x))
            features_1.extend(extract_features(tk_y))
            features_1.extend(extract_features(tk_z))
            
            features_2 = []
            features_2.extend(extract_features(sk_xyz))
            features_2.extend(extract_features(th_xyz))
            features_2.extend(extract_features(tk_xyz))

            features_3 = []
            features_3.extend(extract_features(all_imu))

            
            fft_features_1 = []
            fft_features_1.extend(extract_features(fft_sk_xyz))
            fft_features_1.extend(extract_features(fft_th_xyz))
            fft_features_1.extend(extract_features(fft_tk_xyz))
            

            fft_features_2 = []
            fft_features_2.extend(extract_features(fft_all_imu))
            

            new_df.loc[k,'Timestep'] = k
            new_df.loc[k, new_features] = features_1
            new_df.loc[k, new_features_2] = features_2
            new_df.loc[k, new_features_3] = features_3
            new_df.loc[k, new_fft_features] = fft_features_1
            new_df.loc[k, new_fft_features_2] = fft_features_2
            new_df.loc[k, label]  = 1 if np.mean(df['FoG'][k:k+WINDOW]) > 0.1 else 0
            k += STEP_SIZE
        #normalize the data
        scaled_features = scaler.fit_transform(df)
        #new_df.dropna(inplace=True)
        #save the csv file
        csv_file = out_dir + filename
        new_df.to_csv(csv_file, index=False)
        print('Saved: ', csv_file)
