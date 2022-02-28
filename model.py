import numpy as np
import math


class Evolution:

    def __init__(self):
        self.activation_level = 0.175
        self.input_layer_size = 5
        self.hide_layer_size = 1
        self.out_layer_size = 2
        self.max_w = 10
        self.const_to_mutate = 2  # скок менять весов
        self.mutation_rate = 0.05 # на скок менять рандомно один вес
        self.cross_val_tune = 5  # скок мержить при смешении
        self.w1 = np.matrix(np.random.rand(self.hide_layer_size, self.input_layer_size))
        self.w2 = np.matrix(np.random.rand(self.out_layer_size, self.input_layer_size))

    def sigmoid(self, x):

        s = 1 / (1 + np.exp(-scale(x)))
        return s

    def get_output(self, dist):
        # min max dist to 0..1
        min_max_dist = [1 - i / 250 for i in dist]
        # print(min_max_dist)
        # calculating hide layer
        # hide_layer_calculated = np.matrix([[0.0] for _ in range(self.hide_layer_size)])
        # for i, el in enumerate(min_max_dist):
        #    hide_layer_calculated += el * self.w1[:, i]
        ##print(hide_layer_calculated)

        ## min max layer to 0..1
        # hide_layer_calculated /= self.input_layer_size
        # calculating output layer
        output_layer_calculated = np.matrix([[0.0] for _ in range(self.out_layer_size)])
        for i, el in enumerate(min_max_dist):
            output_layer_calculated += float(el) * self.w2[:, i]

        # min max layer to 0..1
        output_layer_calculated /= self.input_layer_size
        # print([float(i) for i in output_layer_calculated])
        return self.convert_activator_to_boolean([(float(i)) for i in output_layer_calculated])

    def convert_activator_to_boolean(self, activator):
        # print(activator)
        return [True if el > self.activation_level else False for el in activator]

    def make_evolution(self):
        if np.random.randint(100) % 2 == 1:
            t = -1
        else:
            t = 1
        self.activation_level += t * 0.005
        for _ in range(self.const_to_mutate):
            if np.random.randint(100) % 2 == 1:
                t = -1
            else:
                t = 1
            f_index, s_index = np.random.randint(self.out_layer_size), np.random.randint(self.input_layer_size)
            if self.w2[f_index, s_index] - t * self.mutation_rate > 0 and self.w2[
                f_index, s_index] + t * self.mutation_rate < 1:
                self.w2[f_index, s_index] += (t * self.mutation_rate)



    def set_w(self, w):
        self.w1 = w[0]
        self.w2 = w[1]

    def tune_models(self, model):
        for i in range(self.cross_val_tune):
            f_index, s_index = np.random.randint(self.hide_layer_size), np.random.randint(self.input_layer_size)

            self.w1[f_index, s_index] = model.w1[f_index, s_index]


def scale(x):
    return (((x) * (10 - (-10)) / (1)) + -10)
