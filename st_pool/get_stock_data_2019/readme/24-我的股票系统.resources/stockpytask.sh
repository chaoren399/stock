#!/bin/bash
cd  /test/Python-2.7.10 
source stock/bin/activate
echo "source stock/bin/activate" 

cd /zzy/python-workspace/stock/st_pool/agetdata
echo "python 05-getdata.py "
python 05-agetdata.py



deactivate