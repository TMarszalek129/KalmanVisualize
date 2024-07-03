import numpy as np


def generate_cov_matrix(dim : int, scale: float = 1):
    
    cov_matrix = list()
    
    for i in range(dim):
        var1 = np.abs( scale * np.random.randn())
        var2 = np.abs( scale * np.random.randn())
        size = np.sqrt(var1 * var2)
        
        cov = 2 * size * np.random.random_sample() - size
        
        cov_unit = [[var1, cov], [cov, var2]]
        cov_matrix.append(cov_unit)
    
    
    
    return np.array(cov_matrix)