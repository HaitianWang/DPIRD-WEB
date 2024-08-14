# custom_layers.py

from tensorflow.keras.layers import Layer
import tensorflow as tf

class ResizeLayer(Layer):
    def __init__(self, target_height, target_width, **kwargs):
        super(ResizeLayer, self).__init__(**kwargs)
        self.target_height = target_height
        self.target_width = target_width

    def call(self, inputs):
        return tf.image.resize(inputs, (self.target_height, self.target_width))

class ReluLayer(Layer):
    def call(self, inputs):
        return tf.nn.relu(inputs)

# Dictionary of custom objects
custom_objects = {
    'ResizeLayer': ResizeLayer,
    'ReluLayer': ReluLayer
}