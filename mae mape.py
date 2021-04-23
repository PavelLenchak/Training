import numpy as np
from sklearn.metrics import mean_absolute_error as mae

y = np.array([1,2,3,4,5,-1,-2,-3,-4,-5])
y_pred = np.array([0,2,2,5,3,-1,-1,-4,-6,-5])

def mape(y, y_pred): 
    return np.mean(np.abs((y - y_pred) / y)) * 100

print(mae(y, y_pred))
print(mape(y, y_pred))