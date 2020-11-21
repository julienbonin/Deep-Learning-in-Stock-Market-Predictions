import matplotlib.pyplot as plt
import numpy as np

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


def visualize_accuracy(lr_model_history):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.plot(np.sqrt(lr_model_history.history['loss']), 'r', label='train')
    ax.plot(np.sqrt(lr_model_history.history['val_loss']), 'b', label='val')
    ax.set_xlabel(r'Epoch', fontsize=20)
    ax.set_ylabel(r'Loss', fontsize=20)
    ax.legend()
    ax.tick_params(labelsize=20)