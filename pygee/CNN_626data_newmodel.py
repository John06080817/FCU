# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 23:43:05 2018

@author: DaSHitZun
"""

from keras.applications.inception_v3 import InceptionV3, decode_predictions, preprocess_input
from keras.models import Model
from keras.models import load_model
from keras.layers import Dense, GlobalAveragePooling2D,Dropout,Flatten,Input
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import EarlyStopping
import numpy as np
import matplotlib.pyplot as plt  
from keras.models import Sequential
from sklearn.metrics import confusion_matrix
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.vis_utils import plot_model
from keras.optimizers import Adagrad,Adadelta
# 数据准备

train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_batch_size = 150
validation_batch_size = 64


train_generator = train_datagen.flow_from_directory(directory='D:/626alldata_newpoint/train/',
                                  target_size=(80,260),#Inception V3规定大小
                                  batch_size=train_batch_size)
val_generator = val_datagen.flow_from_directory(directory='D:/626alldata_newpoint/validation/',
                                target_size=(80,260),
                                batch_size=validation_batch_size,
                                shuffle=False)

train_generator_confusion = train_datagen.flow_from_directory(directory='D:/626alldata_newpoint/train/',
                                  target_size=(80,260),#Inception V3规定大小
                                  batch_size=train_batch_size,
                                  shuffle=False)
               

input_shape = (80, 260,3)


inputs =Input(input_shape)
conv1 = Conv2D(32, (2, 2), activation='relu',padding ='same')(inputs)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
conv2 = Conv2D(64, (2, 2), activation='relu',padding ='same')(pool1)
pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
conv3 = Conv2D(128, (2, 2), activation='relu',padding ='same')(pool2)
pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
conv4 = Conv2D(256, (2, 2), activation='relu',padding ='same')(pool3)

flat = Flatten()(conv4)
fc1 = Dense(1024, activation='relu')(flat)
drop1 =  Dropout(0.25)(fc1)
fc2 = Dense(626, activation='softmax')(drop1)

model = Model(input = inputs, output = fc2)
print(model.summary())




model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
early_stopping = EarlyStopping(monitor='val_acc', patience=3, verbose=1)

train_history = model.fit_generator(generator=train_generator,
                                  steps_per_epoch=round(626*98*22*0.8/train_batch_size),
                                  epochs=10,
                                  validation_data=val_generator,
                                  validation_steps=round(len(val_generator.filenames)/train_batch_size),
                                  class_weight='auto',
                                  callbacks=[early_stopping])

try:
    model.save('./EMI_CNN14_626alldata_newpoint.h5')
    model.save_weights('./EMI_CNN14_626alldata_newpoint_weights.h5')
    print("Saved model and weights to disk")
    
    
#==============================================================================
#     def show_train_history_acc(train_history, train, validation):  
#         plt.plot(train_history.history[train])  
#         plt.plot(train_history.history[validation])  
#         plt.title('Train History(accuracy)')  
#         plt.ylabel(train)  
#         plt.xlabel('Epoch')  
#         plt.legend(['train', 'validation'], loc='upper left')
#         plt.show()  
#         
#     def show_train_history_loss(train_history, train, validation):  
#         plt.plot(train_history.history[train])  
#         plt.plot(train_history.history[validation])  
#         plt.title('Train History(loss)')  
#         plt.ylabel(train)  
#         plt.xlabel('Epoch')  
#         plt.legend(['train', 'validation'], loc='upper left')
#         plt.show()  
#     print("train_history(accuraty)")
#     show_train_history_acc(train_history, 'acc', 'val_acc')
#     print("train_history(loss)")
#     show_train_history_loss(train_history, 'loss', 'val_loss')
#     
#==============================================================================
    
    
    import csv
    with open('train_history_EMI_CNN14_626alldata_newpoint.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in train_history.history.items():
           writer.writerow([key, value])
except:
    model.save('./EMI_CNN14_626alldata_newpoint.h5')
    model.save_weights('./EMI_CNN14_626alldata_newpoint_weights.h5')
    print("錯誤後 Saved model and weights to disk")



Y_pred = model.predict_generator(val_generator, len(val_generator.filenames)/validation_batch_size )
y_pred = np.argmax(Y_pred, axis=1)



print("\t[Info] Display Confusion Matrix:")  
import pandas as pd  
#==============================================================================
# print("val_generator.classes=",len(val_generator.classes))
# print(" ")
# print("y_pred=",len(y_pred))
# print("%s\n" % pd.crosstab(val_generator.classes, y_pred, rownames=['label'], colnames=['predict']))  
# 
#==============================================================================
print("save confusion matrix")
confusion = pd.crosstab(val_generator.classes, y_pred, rownames=['label'], colnames=['predict'])
confusion.to_csv('confusion_EMI_CNN14_626alldata_newpoint.csv')




x_pred = model.predict_generator(train_generator_confusion, len(train_generator_confusion.filenames)/train_batch_size )
x_pred = np.argmax(x_pred, axis=1)


print("\t[Info] Display Confusion Matrix:")  
print("save confusion matrix")
confusion_x = pd.crosstab(train_generator_confusion.classes, x_pred, rownames=['label'], colnames=['predict'])
confusion_x.to_csv('confusion_train_EMI_CNN14_626alldata_newpoint.csv')

