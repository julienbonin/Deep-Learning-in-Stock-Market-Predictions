import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

df = pd.read_csv("cleaning_data/qqqqqqqqqqqqqqqq.csv")

train_size = int(len(df) * 0.50)
test_size = len(df) - train_size
#
train, test = df.iloc[0:train_size], df.iloc[train_size:len(df)]
test_df = test
# print(len(train), len(test))
#
time_steps = 250
test_time_steps = 250
#
# # # reshape to [samples, time_steps, n_features]
train = train.drop(columns=['date'])
train = train.to_numpy()
scaler = MinMaxScaler(feature_range=(0, 1))
train = scaler.fit_transform(train)
train = pd.DataFrame(data=train)
#
test = test.drop(columns=['date'])
test = test.to_numpy()
scaler = MinMaxScaler(feature_range=(0, 1))
test = scaler.fit_transform(test)
test = pd.DataFrame(data=test)



def create_dataset(X, y, time_steps):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        ys.append(y.iloc[i + time_steps])
    return np.array(Xs), np.array(ys)



# print(len(test))
# if len(test) <= time_steps:
#     test_time_steps = len(test) - 1
#     print(test_time_steps)
#
X_train, y_train = create_dataset(train, train[3], time_steps)
X_test, y_test = create_dataset(test, test[3], 1)
#
# print(len(test))
# print(X_train.shape, y_train.shape)
print(X_test)
print(y_test)

split_fraction = 0.725
train_split = int(split_fraction * int(df.shape[0]))
step = 10

#
# ignore this...for gpu training only
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
tf.config.experimental.set_virtual_device_configuration(gpus[0], [
    tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])

dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    data=test.index,
    targets=test[3],
    sequence_length=10,
    sampling_rate=1,
    batch_size=64,
)
print("data", dataset_val)
#
#
inputs = keras.layers.Input(shape=(X_train.shape[1], X_train.shape[2]))
lstm_out = keras.layers.LSTM(len(train))(inputs)
outputs = keras.layers.Dense(1)(lstm_out)
#
model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss="mse")
model.summary()

path_checkpoint = "model_checkpoints\checkpoint.h5"

modelckpt_callback = keras.callbacks.ModelCheckpoint(
    monitor="val_loss",
    filepath=path_checkpoint,
    verbose=1,
    save_weights_only=False,
    save_best_only=False,
)
#
history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=16,
    validation_split=0.25,
    validation_data=dataset_val,
    verbose=1,
    shuffle=False,
    callbacks=modelckpt_callback,
)


def visualize_loss(history, title):
    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(len(loss))
    plt.figure()
    plt.plot(epochs, loss, "b", label="Training loss")
    plt.plot(epochs, val_loss, "r", label="Validation loss")
    plt.title(title)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


#
visualize_loss(history, "Training and Validation Loss")

df = df.drop(columns=['date'])
small_df = df[-389:]
X_test = create_dataset(small_df, small_df['4. close'], 1)

y_pred = model.predict(X_test)
scaler.min_, scaler.scale_ = scaler.min_[0], scaler.scale_[0]

predictions = scaler.inverse_transform(y_pred)
print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
predictions_df = pd.DataFrame(data=predictions)
final_index = df.index[-1]

predictions_df['new_index'] = predictions_df.index + final_index
predictions_df = predictions_df.set_index('new_index')
predictions_df['new_col'] = predictions_df[0]



plt.figure(figsize=(10, 6))
plt.plot(df['4. close'], color='blue', label='Actual Apple Stock Price')
plt.plot(predictions_df[0], color='red', label='Predicted Apple Stock Price')
# plt.plot(predictions_df['new_col'].rolling(5).mean(), color='green', label='Mean of Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()
