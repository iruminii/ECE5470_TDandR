# test prediction

# Mute tensorflow debugging information on console
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#from flask import Flask, request, render_template, jsonify
from scipy.misc import imsave, imread, imresize
import numpy as np
#import argparse
from keras.models import model_from_yaml
import re
import base64
import pickle
import cv2

def load_model(path):
    ''' Load model from .yaml and the weights from .h5
        Arguments:
            bin_dir: The directory of the bin (normally bin/)
        Returns:
            Loaded model from file
    '''

    # path = model.h5 path

    # load YAML and create model
    yamlpath = r'C:\Users\Oikawa\Desktop\Keras\bin\model.yaml'
    yaml_file = open(yamlpath, 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    model = model_from_yaml(loaded_model_yaml)

    # load weights into new model
    model.load_weights(path)

    return model

def predict(impath, mapping, model):
    ''' Called when user presses the predict button.
        Processes the canvas and handles the image.
        Passes the loaded image into the neural network and it makes
        class prediction.
    '''

    # Local functions
    def crop(x):
        # Experimental
        _len = len(x) - 1
        for index, row in enumerate(x[::-1]):
            z_flag = False
            for item in row:
                if item != 0:
                    z_flag = True
                    break
            if z_flag == False:
                x = np.delete(x, _len - index, 0)
        return x

    def parseImage(imgData):
        # parse canvas bytes and save as output.png
        imgstr = re.search(b'base64,(.*)', imgData).group(1)
        with open('output.png','wb') as output:
            output.write(base64.decodebytes(imgstr))



    # get data from drawing canvas and save as image
    #parseImage(request.get_data())

    # read parsed image back in 8-bit, black and white mode (L)
    x = imread(impath, mode='L')

    ### Experimental
    # Crop on rows
    # x = crop(x)
    # x = x.T
    # Crop on columns
    # x = crop(x)
    # x = x.T

    # Visualize new array
    imsave('resized.png', x)

    x = imresize(x,(28,28))

    # reshape image data for use in neural network
    x = x.reshape(1,28,28,1)

    # Convert type to float32
    x = x.astype('float32')
    # Normalize to prevent issues with model
    x /= 255

    # Predict from model
    out = model.predict(x)

    # Generate response
    # Generate response
    #response = {'prediction': chr(mapping[(int(np.argmax(out, axis=1)[0]))]),
    #            'confidence': str(max(out[0]) * 100)[:6]}
    response = chr(mapping[(int(np.argmax(out, axis=1)[0]))])

    #print('character: ' + response + ' / confidence: ' + str(max(out[0]) * 100)[:6])

    #print("response = ", response)
    return response
    #return jsonify(response)

#if __name__ == '__main__':
def guesstext():
    # mapping path
    mpath = r'C:\Users\Oikawa\Desktop\Keras\bin\mapping.p'
    # maps prediction to label
    mapping = pickle.load(open(mpath, 'rb'))

    # model path
    path = r'C:\Users\Oikawa\Desktop\Keras\bin\model.h5'
    #load model
    model = load_model(path)

    #image folder path
    #imfilepath = r'C:\Users\Oikawa\Desktop\ECE5470Project\bbroi'
    imfilepath = r'C:\Users\Oikawa\Desktop\ECE5470Project\characters'

    # empty array to hold characters
    predictions = np.array([])
    cnt = 0
    # https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    pred_text = ''
    for filename in os.listdir(imfilepath):
        if filename.endswith(".jpg"):
            # make predictions
            guess = predict(imfilepath + r'\char%d.jpg' % cnt, mapping, model)
            cnt = cnt + 1
            predictions = np.append(predictions, guess)
            continue
        else:
            pred_text = ''.join(predictions)

    print(pred_text)
    return str(pred_text)

string = guesstext()

print(len(string))
print(string)

