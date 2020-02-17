import random
from copy import deepcopy
import tensorflow.keras as keras
import numpy as np
from game_environ import test


def mutate(a):
    b =random.random()*np.random.standard_normal(a.shape)
    return b+a
def mutate_model(model):
    if not random.randint(0,3):
        w = model.get_weights()
        w = np.asarray(w)
        after = mutate(w)
        model.set_weights(after)
        return deepcopy(model)
    else:
        return deepcopy(model)
def normalize(v):
    norm = np.sum(v)
    if norm == 0:
       return v
    return v / norm

class Model:
    def __init__(self,hiddenlayersize,model):
        self.hiddenlayersize = hiddenlayersize
        if not model:
            self.model = keras.models.Sequential([
                keras.layers.Dense(hiddenlayersize,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
            self.model.summary()
        else:
            self.model = model
    def return_mutated(self,n):
        mods = []
        for i in range(n-1):
            mods.append(Model(self.hiddenlayersize,model = mutate_model(self.model)))
        mods.append(self)
        return mods
    def predictt(self,input):
        """
        returns the output given an input
        """
        # print("called")
        
        input = np.array([input[0],input[1][0],input[1][1],input[2][0],input[2][1]])
        input = normalize(input)
        print(input.shape)
        out = self.model.predict(input)
        print(out)
        return out
    def run(self):
        self.runcount = test(self.predictt,True)
model = Model(10,False)
model.run()