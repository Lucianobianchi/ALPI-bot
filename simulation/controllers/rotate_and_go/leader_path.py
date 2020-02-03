import numpy as np

def generate_gerono_lemniscate_t(coords_len):
    p1 = np.arange(0, np.pi + 0.000001, (np.pi)/(coords_len/2))
    p2 = np.arange(-np.pi - 0.000001, 0, (np.pi)/(coords_len/2))
    return np.concatenate((p1, p2))

def gerono_lemniscate_xy(t, A = 1):
    return A * np.sin(t), A * np.sin(t) * np.cos(t)

def generate_bernoulli_lemniscate_t(coords_len):
    p1 = np.arange(np.pi/2, 0, -(np.pi)/(coords_len/2))
    p2 = np.arange(0, -np.pi, -(np.pi)/(coords_len/2))
    p3 = np.arange(np.pi, np.pi/2 - 0.0001, -(np.pi)/(coords_len/2))
    return np.concatenate((p1, p2, p3))

def bernoulli_lemniscate_xy(t, A = 1):
    x = (A * np.sqrt(2) * np.cos(t))/(np.sin(t)**2 + 1)
    y = A * np.sqrt(2) * np.cos(t) * np.sin(t)/(np.sin(t)**2 + 1)
    return x, y