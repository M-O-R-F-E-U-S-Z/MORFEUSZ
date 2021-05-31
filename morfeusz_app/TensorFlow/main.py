import data_manager
import training
import analysis
import logging

CLASSES = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']

layer_sizes = [128]
conv_layers = [4]
dense_layers = [2]
epochs = 30

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    data_manager.create_data()

    training.model(layer_sizes, conv_layers, dense_layers, epochs)
    
    layer_size = layer_sizes[0]
    conv_layer = conv_layers[0]
    dense_layer = dense_layers[0]
    analysis.prediction(layer_size, conv_layer, dense_layer)
