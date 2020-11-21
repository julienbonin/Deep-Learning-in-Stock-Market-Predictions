import tensorflow as tf
from tensorflow import keras
import datetime

model_checkpoint_callback = keras.callbacks.ModelCheckpoint(
    monitor="loss",
    filepath="model_checkpoints/checkpoint02/01.hd5",
    verbose=1,
    save_weights_only=True,
    save_best_only=True,
)

#
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)



early_stopping_callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)