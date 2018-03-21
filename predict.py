import numpy as np
from sigmoid import sigmoid

def predict(Theta1, Theta2, X):
    m = X.shape[0]
    ones = np.ones((m, 1))
    X  = np.c_[ones, X]
    # print(X)
    a2 = np.c_[ones, sigmoid(X * Theta1.T)]
    a3 = sigmoid(a2 * Theta2.T)
    p  = np.argmax(a3, axis=1) + 1

    return p
