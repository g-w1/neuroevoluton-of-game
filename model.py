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
    def __init__(self,hiddenlayersize,model = None):
        self.hiddenlayersize = hiddenlayersize
        if not model:
            self.model = keras.models.Sequential([
                keras.layers.Dense(5,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(hiddenlayersize, activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
    def return_mutated(self,n):
        mods = []
        for i in range(n-1):
            mods.append(Model(self.hiddenlayersize,model = mutate_model(self.model)))
        mods.append(self)
        return mods
    def predict(self,input):
        [world.bodies[5].position[0],world.bodies[4].linearVelocity,world.bodies[4].position]
        input = np.array(input[0],input[1][0],input[1][1],input[2][0],input[2][1])
        input = normalize(input)
        out =  model.predict(input)
        print(out)
        return out
    def run(self):
        self.runcount = test(self.predict,True)
model = Model(10)
model.run()