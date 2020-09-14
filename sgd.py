

#SGD
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
import argparse


def sigmoid_activation(x):
    return 1/(1+np.exp(-x))
def sigmoid_deriv(x):
    return x * (1-x)
def predict(X,W):
    
    preds =sigmoid_activation(X.dot(W))
    
    preds[preds <=0.5] =0
    preds[preds >0] =1
    return preds
def next_batch(X,y, batchSize):
    for i in np.arange(0, X.shape[0], batchSize):
        yield (X[i:i + batchSize], y[i:i + batchSize])
#parsing the argument        
ap =argparse.ArgumentParser()
ap.add_argument("-e", "--epochs", type = float ,  default =100, help ="no of epochs")
ap.add_argument("-a", "--alpha", type = float , default =0.01, help ="learning rate")
ap.add_argument("-b" ,"--batch-size" , type =int , default =128 , help ="mini-batches of the training set")
args =vars(ap.parse_args())

(X,y) = make_blobs(n_samples=1000, n_features =2, cluster_std =1.5, centers= 2, random_state =1)
y = y.reshape((y.shape[0], 1))

X =np.c_[X, np.ones((X.shape[0]))]

(trainX, testX, trainY, testY) = train_test_split(X, y, test_size=0.5, random_state=42)

print("Model is training......")
W = np.random.randn(X.shape[1],1)
losses =[]


#loop over the epochs

for epoch in np.arange(0, args["epochs"]):
    epochLoss = []
# initialize the total loss for the epoch epochLoss = []
    
    for (batchX, batchY) in next_batch(trainX, trainY , args["batch_size"]):
        preds =sigmoid_activation(batchX.dot(W))
        
        
        
        error = preds- batchY
        epochLoss.append(np.sum(error ** 2))
        
        
        d= error*sigmoid_deriv(preds)
        gradient =batchX.T.dot(d)
        
        W += -args["alpha"] * gradient
        
        
        loss = np.average(epochLoss)
        losses.append(loss)
    
# check to see if an update should be displayed
        if epoch == 0 or (epoch + 1) % 5 == 0:
            print("[INFO] epoch={}, loss={:.7f}".format(int(epoch + 1), loss))
            
        
print("Model is evaluating....")
preds = predict(testX, W)
print(classification_report(testY, preds))

plt.style.use("ggplot")
plt.figure()
plt.title("Data")
plt.scatter(testX[:, 0], testX[:, 1], marker="o", c=testY[:, 0], s=30)

# construct a figure that plots the loss over time
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, args["epochs"]), losses)
plt.title("Training loss")
plt.xlabel("epochs")
plt.ylabel("loss")

plt.show()

































# In[ ]:




