import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from charting_helpers import *
from tf_calbacks import *

# get data
stock_name_for_charting="Tesla"
df = pd.read_csv("data_csv_GE.csv")
df = df.drop(columns=['date', 'Unnamed: 0'],axis=1)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.fillna(0)

print(df.info())

train_size = int(len(df) * .75)
test_size = len(df) - train_size

train, test = df.iloc[0:train_size], df.iloc[train_size:len(df)]

train = train.to_numpy()
test = test.to_numpy()

scaler = MinMaxScaler(feature_range=(0, 1) )
train = scaler.fit_transform(train)
test = scaler.fit_transform(test)

X_train = np.delete(train,3,1)
y_train = train[:, 3]

X_test = np.delete(test,3,1)
y_test = test[:, 3]

# ignore this...for gpu training only
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
tf.config.experimental.set_virtual_device_configuration(gpus[0], [
    tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3048)])

dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    data=X_train,
    targets=y_train,
    sequence_length=48,
    sampling_rate=1,
    batch_size=389,
)



inputs = keras.layers.Input(shape=(dataset_train.__len__(), 145))
lstm_out = keras.layers.LSTM(145)(inputs)
outputs_1 = keras.layers.Dense(70, activation='relu')(lstm_out)
outputs_2 = keras.layers.Dense(35, activation='linear')(outputs_1)
outputs_3 = keras.layers.Dense(17, activation='linear')(outputs_2)
outputs = keras.layers.Dense(1, activation='linear')(outputs_3)
model = keras.Model(inputs=inputs, outputs=outputs)
model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.001), loss="mse",
              metrics=['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error', 'cosine_proximity'])
model.summary()


print(dataset_train)

# comment this to train new
model.load_weights("model_checkpoints/checkpoint02/01.hd5")


# uncomment this to train
# history = model.fit(
#     dataset_train,
#     epochs=3000,
#     batch_size=240,
#     # validation_split=0.1,
#     # validation_data=dataset_val,
#     verbose=1,
#     shuffle=False,
#     callbacks=[model_checkpoint_callback,tensorboard_callback, early_stopping_callback]
# )
# print(history.history)


# just in case matplotlib doesnt chart properly
df.to_csv("testing_main_data.csv")

dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    data=X_test,
    targets=y_test,
    sequence_length=48,
    sampling_rate=1,
    batch_size=389,
)

print(X_train)
# eval the model or check tensorboard
score = model.evaluate(dataset_train, batch_size=240)
print("test loss, test acc:", score)



small_df = df[-389:]
small_df_col = list(small_df.columns.values)
small_df = small_df.to_numpy()


scaler = MinMaxScaler(feature_range=(0, 1),)
small_df = scaler.fit_transform(small_df)


small_df = pd.DataFrame(data=small_df,columns=small_df_col)


x_small_df = small_df.drop(columns=['4. close'])
y_small_df = small_df['4. close']


# save to df for testing
small_df.to_csv("testing_pred_xsmall_data.csv")

dataset_val = keras.preprocessing.timeseries_dataset_from_array(
    data=x_small_df,
    targets=y_small_df,
    sequence_length=48,
    sampling_rate=1,
    batch_size=389,
)

y_pred = model.predict(dataset_val)



scaler.min_, scaler.scale_ = scaler.min_[0], scaler.scale_[0]

predictions = scaler.inverse_transform(y_pred)

print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
predictions_df = pd.DataFrame(data=predictions)
final_index = df.index[-1]

##adjust timeshift for plotting on top of one another
predictions_df['new_index'] = predictions_df.index + final_index - (len(predictions_df) + 25)
predictions_df = predictions_df.set_index('new_index')
predictions_df['new_col'] = predictions_df[0]

predictions_df.to_csv("testing_pred_data.csv")


plt.figure(figsize=(10, 6))
plt.plot(df['4. close'][-778:], color='blue', label='Actual '+stock_name_for_charting+' Stock Price')
plt.plot(df['4. close'][-389:].ewm(span = 25).mean(), color='orange', label='100 Timestamp Mean of '+stock_name_for_charting+' Stock Price')
plt.plot(predictions_df['new_col'], color='red', label='Predicted '+stock_name_for_charting+' Stock Price')
plt.plot(predictions_df['new_col'].ewm(span=25).mean(), color='green', label='Mean of Predicted '+stock_name_for_charting+' Stock Price')

z = np.polyfit(predictions_df.index, predictions_df['new_col'].ewm(span=25).mean(), 1)
p = np.poly1d(z)
plt.plot(predictions_df.index,p(predictions_df.index),"r--")


plt.title(stock_name_for_charting+' Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel(stock_name_for_charting+' Stock Price')
plt.legend()
plt.show()

print(z[0])