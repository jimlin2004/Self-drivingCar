import tensorflow as tf

model = tf.keras.models.load_model("model_keras.h5")
print(model.summary())
model.save("model_keras")
