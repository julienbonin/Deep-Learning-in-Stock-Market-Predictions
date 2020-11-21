import pandas as pd
import matplotlib.pyplot as plt
from indicator_imp import calc_indicators



df = pd.read_csv("data_csv.csv")

df= calc_indicators(df)
df = df.reset_index()


titles = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "SMA Open",
    "EMA Open",
    "MACD",
    "MFI",
    "RSI"

]

feature_keys = [
    "1. open",
    "2. high",
    "3. low",
    "4. close",
    "5. volume",
    "sma_open_389",
    "ema_open_389",
    "macd_389_2",
    "MFI_389",
    "RSI_2"
]

colors = [
    "blue",
    "orange",
    "green",
    "red",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",

]

date_time_key = "date"


def show_raw_visualization(data):
    time_data = data.index
    fig, axes = plt.subplots(
        nrows=5, ncols=2, figsize=(10, 15), dpi=80, facecolor="w", edgecolor="k"
    )
    for i in range(len(feature_keys)):
        key = feature_keys[i]
        c = colors[i % (len(colors))]
        t_data = data[key]
        t_data.index = time_data
        t_data.head()

        ax = t_data.plot(
            ax=axes[i // 2, i % 2],
            color=c,
            title="{} - {}".format(titles[i], key),
            rot=25,
        )
        ax.legend([titles[i]])
    plt.tight_layout()
    plt.show()


show_raw_visualization(df)



# def show_heatmap(data):
#     plt.matshow(data.corr())
#     # plt.xticks(range(data.shape[1]), data.columns[:10], fontsize=10, rotation=90)
#     # plt.gca().xaxis.tick_bottom()
#     # plt.yticks(range(data.shape[1]), data.columns[:10], fontsize=10)
#     #
#     # cb = plt.colorbar()
#     # cb.ax.tick_params(labelsize=14)
#     plt.title("Feature Correlation Heatmap", fontsize=14)
#     plt.show()


# show_heatmap(df)


# import tensorflow as tf
#
# input = tf.keras.Input(shape=(100,), dtype='int32', name='input')
# x = tf.keras.layers.Embedding(
#     output_dim=512, input_dim=10000, input_length=100)(input)
# x = tf.keras.layers.LSTM(32)(x)
# x = tf.keras.layers.Dense(64, activation='relu')(x)
# x = tf.keras.layers.Dense(64, activation='relu')(x)
# x = tf.keras.layers.Dense(64, activation='relu')(x)
# output = tf.keras.layers.Dense(1, activation='sigmoid', name='output')(x)
# model = tf.keras.Model(inputs=[input], outputs=[output])
# dot_img_file = '/tmp/model_1.png'
# tf.keras.utils.plot_model(model, to_file=dot_img_file, show_shapes=True)