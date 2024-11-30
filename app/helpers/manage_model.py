import tensorflow as tf
def LoadModel():
    path_model = "./model/obesity_prediction_model.h5"
    model = tf.keras.models.load_model(path_model)
    return model