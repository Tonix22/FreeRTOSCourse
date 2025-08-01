## Create an image


```
docker build -t esp-idf .
```



### Add the usb device 

Verify fist the usb is ready and have enought privileges

```
ls /dev/ttyUSB*
chmod 777 /dev/ttyUSB0
sudo usermod -aG dialout $USER
```


```
docker run -it --rm --device=/dev/ttyUSB0 -v $(pwd):/project esp-idf
```

## Run container in a project

```
docker run -it --rm -v $(pwd):/project esp-idf
```

## Build 

```
idf.py set-target esp32
idf.py build
```