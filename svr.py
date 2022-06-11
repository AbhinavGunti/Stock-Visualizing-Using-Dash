#1 Importing the libraries
from sqlite3 import Date
from tokenize import String
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

#2 Importing the dataset
end_date = datetime.today()
end_date=end_date.strftime("%Y-%m-%d")
start_date = datetime.today() - timedelta(days=20)
start_date=start_date.strftime("%Y-%m-%d")
# print(type(start_date),end_date)
df = yf.download("AAPL",start_date,end_date)
df.reset_index(inplace=True)
print(df)


# # dataset = pd.read_csv('Position_Salaries.csv')
X = df.iloc[:,0:1].values.astype(str)
y = df.iloc[:,4:5].values.astype(float)
print("X : \n",X)
print("\ny : \n",y)
#3 Feature Scaling
# from sklearn.preprocessing import StandardScaler
# sc_X = StandardScaler()
# sc_y = StandardScaler()
# X = sc_X.fit_transform(X)
# y = sc_y.fit_transform(y)
# #4 Fitting the Support Vector Regression Model to the dataset
# # Create your support vector regressor here
# from sklearn.svm import SVR
# # most important SVR parameter is Kernel type. It can be #linear,polynomial or gaussian SVR. We have a non-linear condition #so we can select polynomial or gaussian but here we select RBF(a #gaussian type) kernel.
# regressor = SVR(kernel='rbf')
# regressor.fit(X,y)
# #5 Predicting a new result
# y_pred = sc_y.inverse_transform ((regressor.predict (sc_X.transform(np.array([[6.5]])))))
# #6 Visualising the Regression results (for higher resolution and #smoother curve)
# X_grid = np.arange(min(X), max(X), 0.1)
# X_grid = X_grid.reshape((len(X_grid), 1))
# plt.scatter(X, y, color = 'red')
# plt.plot(X_grid, regressor.predict(X_grid), color ='blue')
# plt.title('Truth or Bluff (Support Vector Regression Model(High Resolution))')
# plt.xlabel('Position level')
# plt.ylabel('Salary')
# plt.show()