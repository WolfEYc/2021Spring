from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

df = pd.read_csv('heart.csv')

dead_df = df[df['DEATH_EVENT']==1][0:300]
alive_df = df[df['DEATH_EVENT']==0][0:300]

axes = dead_df.plot(kind='scatter', x='ejection_fraction', y='serum_creatinine',color='red', label='dead patients')
alive_df.plot(kind='scatter', x='ejection_fraction', y='serum_creatinine',color='blue', label='alive patients', ax=axes)

df.columns
feature_df = df[['ejection_fraction','serum_creatinine']]

X = np.asarray(feature_df)
y = np.asarray(df['DEATH_EVENT'])

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2)

linear_svc = svm.SVC(kernel='linear',random_state=1).fit(X_train,y_train)
rbf_svc = svm.SVC(kernel='rbf',random_state=2).fit(X_train,y_train)

relu_MLP = MLPClassifier(activation='relu',max_iter=300,random_state=3).fit(X_train,y_train)
tanh_MLP = MLPClassifier(activation='tanh',max_iter=300,random_state=4).fit(X_train,y_train)

linear_y_predict = linear_svc.predict(X_test)
rbf_y_predict = rbf_svc.predict(X_test)
relu_y_predict = relu_MLP.predict(X_test)
tanh_y_predict = tanh_MLP.predict(X_test)

print('\nLinear Kernel')
print('accuracy:',int(100*linear_svc.score(X_test,y_test)),'%')
print(classification_report(y_test,linear_y_predict))

print('\nRBF Kernel')
print('accuracy:',int(100*rbf_svc.score(X_test,y_test)),'%')
print(classification_report(y_test,rbf_y_predict))

print('\nRelu MLP')
print('accuracy:',int(100*relu_MLP.score(X_test,y_test)),'%')
print(classification_report(y_test,relu_y_predict))

print('\nTanh MLP')
print('accuracy:',int(100*relu_MLP.score(X_test,y_test)),'%')
print(classification_report(y_test,tanh_y_predict))

plt.show()