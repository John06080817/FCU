使用方法

一、ASM2o.py  (組譯器)

python ASM2o.py 組合語言檔案

ex：python ASM2o.py c1.s

二、o2bin.py  (鏈結器)

python o2bin.py 檔案一 檔案二 ... 檔案N 輸出檔名

ex：python o2bin.py c1.0 c0.o c3.o test

三、測試

python ASM2o.py c1.s  (產生c1.o)
python ASM2o.py c0.s  (產生c0.o)
python o2bin.py c1.o c0.o test  (產生test.bin)