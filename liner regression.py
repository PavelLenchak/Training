from sklearn import linear_model as lm
# Create linear regression object
lr = lm.LinearRegression()
lr.fit([[0],[1],[2],[3]], [0,1,0,3])
print("Intercept: ", lr.intercept_)
print("Coefficient: ", lr.coef_)