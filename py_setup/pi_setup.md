## Setup 

raspberry pi Image: 

increase swap (https://pimylifeup.com/raspberry-pi-swap-file/)
    sudo nano /etc/dphys-swapfile
    CONF_SWAPSIZE=1024

    copy to micro = strg + shift + v 

install editor micro https://lindevs.com/install-micro-text-editor-on-raspberry-pi/

instal all python Dependencies 
    sudo apt-get install -y python-picamera python3-picamera python3-numpy python3-matplotlib python3-pil.imagetk python3-pip python3-pyqt5

    pip3 install jupyter
        maybe  add "export PATH=$PATH:~/.local/bin"maybe 




from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image

# Create the in-memory stream
stream = BytesIO()
camera = PiCamera()
camera.start_preview()
sleep(2)
camera.capture(stream, format='jpeg')
# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)


python3 -m pip install -U pip
python3 -m pip install -U scikit-image
python3 -m pip install -U scikit-image[optional]

## link nupy to openBLAS
https://stackoverflow.com/questions/21671040/link-atlas-mkl-to-an-installed-numpy

show current linking: 
    ldd -v /home/pi/.local/lib/python3.7/site-packages/numpy/core/_multiarray_umath.cpython-37m-arm-linux-gnueabihf.so
atlas blas
    /lib/arm-linux-gnueabihf/libatlas.so.3 (0x769cd000)

get file info(not location) with apt-get
    apt-cache show libopenblas-base

find any file in system:
    sudo find / -name '*libblas.so'


link :  /usr/lib/libblas.so.3 \     (symlink)
name:   libblas.so.3 \              (generic name for the master link)
path:   /opt/OpenBLAS/lib/libopenblas.so \ (alternative being introduced for the master link)
priotryti : 50 (hight the early taken) 