call conda activate

D:

cd D:\20.share\BHRC\py_script\py\SEC02T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC04T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC05T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC06T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC07T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC09T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC11T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC12T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC14T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC51T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC03T
python main.py
timeout /t 5

cd D:\20.share\BHRC\py_script\py\SEC31T
python main.py
timeout /t 5

goto :start

cd D:\20.share\BHRC\py_script\py\SEC99T
python main.py
timeout /t 5

:start

call conda deactivate