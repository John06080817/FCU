# -*- coding: utf-8 -*-
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer

#將html的標籤刪除
import re
def rm_tags(text):
    re_tag = re.compile(r'<[^>]+>')
    return re_tag.sub('', text)

#讀取IMDb的檔案目錄
import os
def read_files(filetype):
    path = "aclImdb/"
    file_list=[]

    positive_path=path + filetype+"/pos/"
    for f in os.listdir(positive_path):
        file_list+=[positive_path+f]
    
    negative_path=path + filetype+"/neg/"
    for f in os.listdir(negative_path):
        file_list+=[negative_path+f]
        
    print('read',filetype, 'files:',len(file_list))
       
    all_labels = ([1] * 12500 + [0] * 12500) 
    
    all_texts  = []
    for fi in file_list:
        with open(fi,encoding='utf8') as file_input:
            all_texts += [rm_tags(" ".join(file_input.readlines()))]
            
    return all_labels,all_texts

y_train, train_text = read_files("train")
y_test, test_text = read_files("test")

token = Tokenizer(num_words=3800)
token.fit_on_texts(train_text)

x_train_seq = token.texts_to_sequences(train_text)
x_test_seq = token.texts_to_sequences(test_text)

x_train = sequence.pad_sequences(x_train_seq, maxlen = 380)
x_test = sequence.pad_sequences(x_test_seq, maxlen = 380)

from keras.models import Sequential
from keras.layers.core import Dense, Dropout,Activation,Flatten
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM

###建立線性堆疊模型
model=Sequential()
model.add(Embedding(output_dim=32,
                   input_dim=3800,
                   input_length=380))
model.add(Dropout(0.2))
model.add(LSTM(48))
model.add(Dense(units=256,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=1,activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

train_history=model.fit(x_train,y_train,validation_split=0.2,epochs=15,batch_size=1000,verbose=1)

scores=model.evaluate(x_test,y_test)
print(scores[1])