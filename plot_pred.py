import pandas as pd
import matplotlib.pyplot as plt
# from tensorflow.keras.models import load_model
# import tensorflow as tf
# from tensorflow import keras
import numpy as np
#
#
#
#
 ##creat_dataset
# def create_dataset(X, y, time_steps):
#  Xs, ys = [], []
#  for i in range(len(X) - time_steps):
#      v = X.iloc[i:(i + time_steps)].values
#      Xs.append(v)
#      ys.append(y.iloc[i + time_steps])
#  return np.array(Xs).astype('float32'), np.array(ys).astype('float32')
# #
# #
# #
# # model = keras.models.load_model("model_checkpoints/checkpoint/132.h5")
#
#
# ##get data
# df=pd.read_csv("kk.csv")
# print(df.tail())
#
# # df = df.drop(columns=['date'])
# # small_df = df[-389:]
#
# # X_test = create_dataset(small_df, small_df['4. close'], 1)
#
# # y_pred = model.predict(small_df['4. close'])
# # # scaler.min_, scaler.scale_ = scaler.min_[0], scaler.scale_[0]
# #
# # # predictions = scaler.inverse_transform(y_pred)
# # print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
# predictions_df=pd.read_csv("testing_pred_data.csv",index_col='new_index')
# final_index = df.index[-1]
#
# predictions_df['new_index'] = predictions_df.index-389
# predictions_df = predictions_df.set_index('new_index')
# print(predictions_df.tail())
# predictions_df['new_col'] = predictions_df['0']
#
# #
# #
# # df['4. close'].to_csv("testing_main_data.csv")
#
# #
# #
# # plt.figure(figsize=(10, 6))
#
# print(df.tail())
# print(predictions_df.tail())
#

#
#
#
#
#
#
# model.fit
# get data
df = pd.read_csv("data_csv.csv")
df= df.drop(columns=['date','Unnamed: 0'])
df =df.fillna(0)



# model = keras.models.load_model("model_checkpoints\\checkpoint\\max.h5")

# small_df = df[-389:]
# small_df = create_dataset()
# small_df.predict

pred_df = pd.read_csv('testing_pred_data.csv')
pred_df.index = df.index[-389:]


plt.plot(df['4. close'][-390:], color='blue', label='Actual Apple Stock Price')
plt.plot(pred_df['0'], color='red', label='Predicted Apple Stock Price')
plt.plot(pred_df['0'].rolling(50).mean(), color='green', label='Mean of Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()



