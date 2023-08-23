import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import lightgbm as lgb
import scipy.signal as sig
from sklearn.metrics import balanced_accuracy_score

# Charger le modèle entraîné
model = lgb.Booster(model_file='trained_model.txt')

# Définir votre fenêtre glissante
WINDOW_SIZE = 1000
TRESHOLD = 0.45
REPARTITION = 0.114285714

# Charger les données de test
test_data = pd.read_csv('test/S07R01_1.csv')  # Remplacez 'test_data.csv' par votre propre fichier de test
# Prétraiter les données de test si nécessaire
# test_data = preprocess(test_data)
features = ['Shank_x', 'Shank_y', 'Shank_z', 'Thigh_x', 'Thigh_y', 'Thigh_z', 'Trunk_x', 'Trunk_y', 'Trunk_z', 'Shank_mean', 'Thigh_mean', 'Trunk_mean', 'MEAN']
time = np.arange(0, WINDOW_SIZE)
time = (time/64)
X_test = np.array(test_data[features][:WINDOW_SIZE])
#y_test = np.array(test_data['FoG'][k:k + WINDOW_SIZE])
y_pred = model.predict(X_test)
y_valid = np.array(test_data['FoG'][:WINDOW_SIZE])
y_pred_binary = np.where(y_pred > TRESHOLD, 1, 0)

balanced_accuracy = np.zeros(WINDOW_SIZE)
balanced_accuracy = np.delete(balanced_accuracy, 0)
balanced_accuracy = np.append(balanced_accuracy, balanced_accuracy_score(y_valid, y_pred_binary))

#PLOT
fig, ((pred, pred_bin), (bal_accuracy, valid)) = plt.subplots(2, 2, figsize=(13, 7))

# animated=True tells matplotlib to only draw the artist when we
# explicitly request it
(ln,) = pred.plot(time, y_pred*100, animated=True)
(ln2,) = valid.plot(time, y_valid, animated=True)
(ln3,) = pred_bin.plot(time, y_pred_binary, animated=True)
(ln4,) = bal_accuracy.plot(time, balanced_accuracy*100, animated=True)
pred.set_title('FoG Prediction %')
pred.set_ylim(-5, 100)
valid.set_title('FoG Validation')
valid.set_ylim(-0.5, 1.5)
pred_bin.set_title(f'FoG Tresholded : {TRESHOLD}')
pred_bin.set_ylim(-0.5, 1.5)
bal_accuracy.set_title('Balanced Accuracy %')
bal_accuracy.set_ylim(-5, 100)
# make sure the window is raised, but the script keeps going
plt.tight_layout()
plt.show(block=False)

# stop to admire our empty window axes and ensure it is rendered at
# least once.
#
# We need to fully draw the figure at its final size on the screen
# before we continue on so that :
#  a) we have the correctly sized and drawn background to grab
#  b) we have a cached renderer so that ``ax.draw_artist`` works
# so we spin the event loop to let the backend process any pending operations
plt.pause(0.5)

# get copy of entire figure (everything inside fig.bbox) sans animated artist
bg = fig.canvas.copy_from_bbox(fig.bbox)
# draw the animated artist, this uses a cached renderer
pred.draw_artist(ln)
valid.draw_artist(ln2)
# show the result to the screen, this pushes the updated RGBA buffer from the
# renderer to the GUI framework so you can see it
fig.canvas.blit(fig.bbox)

for k in range(61500, len(test_data) - WINDOW_SIZE):
    #print(k)
    X_test = np.array(test_data[features][k:k + WINDOW_SIZE])
    #y_test = np.array(test_data['FoG'][k:k + WINDOW_SIZE])
    y_pred = model.predict(X_test)
    y_pred = sig.savgol_filter(y_pred, (int) (WINDOW_SIZE/20), 2)
    y_valid = np.array(test_data['FoG'][k:k + WINDOW_SIZE])
    y_pred_binary = np.where(y_pred > TRESHOLD, 1, 0)
    balanced_accuracy = np.delete(balanced_accuracy, 0)
    balanced_accuracy = np.append(balanced_accuracy, balanced_accuracy_score(y_valid, y_pred_binary))

    # reset the background back in the canvas state, screen unchanged
    fig.canvas.restore_region(bg)

    # update the artist, neither the canvas state nor the screen have changed
    ln.set_ydata(y_pred*100)
    ln2.set_ydata(y_valid)
    ln3.set_ydata(y_pred_binary)
    ln4.set_ydata(balanced_accuracy*100)

    # re-render the artist, updating the canvas state, but not the screen
    pred.draw_artist(ln)
    valid.draw_artist(ln2)
    pred_bin.draw_artist(ln3)
    bal_accuracy.draw_artist(ln4)

    # copy the image to the GUI state, but screen might not be changed yet
    fig.canvas.blit(fig.bbox)

    # flush any pending GUI events, re-painting the screen if needed
    fig.canvas.flush_events()

    # you can put a pause in if you want to slow things down
    # plt.pause(.1)