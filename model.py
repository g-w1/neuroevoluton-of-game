import random
from copy import deepcopy
import keras
import numpy as np
from game_environ import test


def mutate(a):
    b =random.random()*np.random.standard_normal(a.shape)
    return b+a
def normalize(v):
    norm = np.sum(v)
    if norm == 0:
       return v
    return v / norm

class Model:
    def __init__(self,hiddenlayersize,model,show = True):
        self.hiddenlayersize = hiddenlayersize
        self.show=  show
        if not model:
            self.model = keras.models.Sequential([
                keras.layers.Dense(hiddenlayersize,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
        else:
            self.model = model
    def return_mutated(self,n):
        mods = []
        for i in range(n-1):
            mods.append(Model(self.hiddenlayersize,self.copy_mutate(),show = self.show))
        mods.append(self)
        return mods
    def predictt(self,input):
        """
        returns the output given an input
        """
        input = np.array([input[0],input[1][0],input[1][1],input[2][0],input[2][1]])
        input = normalize(input)
        
        input = input.reshape(1,5)
        out = self.model.predict(input)#do batches!!!!!!!!!!!
        return out
    def run(self,seed):
        self.runcount = test(self.predictt,self.show,seed)
        upplim = 3000
        if self.runcount>upplim:
            self.model.save_weights('model.h5')
            print(f'over {upplim}')
    def copy_mutate(self):
        model = keras.models.Sequential([
                keras.layers.Dense(self.hiddenlayersize,input_shape=(5,), activation='tanh'),
                keras.layers.Dense(1, activation='tanh')
        ])
        model.set_weights([mutate(x) for x in deepcopy(self.model.get_weights())])
        modelc = Model(self.hiddenlayersize,model,show=False)
        return modelc

if __name__ == "__main__":
    from population import createSeed
    model = Model(10,False,show=True)
    model.model.load_weights('model.h5')
    model.run(createSeed())