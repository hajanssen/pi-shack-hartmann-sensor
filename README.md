# Shack–Hartmann wavefront sensor with an Raspberry Pi and the HQ camera module

The Goal of this project is to build an integrated wavefront sensor. With the Raspberry Pi HQ camera, an Lens array and the Raspberry Pi zero 2 W.

![](/docs/img/mounting-plate-for-raspberry-pi-zero-and-hq-camera.jpg "Logo Title Text 1")

With this Setup the Device could maybe have a size of 70mm x 45mm x 40mm
## TO DO List

- build simulator for SHS Images(OOP in Python) [50%]
  - different size of image: NPixel as tuple for x,y or as scaler for quadratic
  - different number of dots/lense: NLens as tuple for x,y or scaler for quadratic

- build algorithm to detect "dots" and calculate shift in image space(~gradient data) [30%]
  - firs measure accuracy/quality
  - second speed, on x86 PC and Raspberry PI Zero 2W
  - consider implementation in C++ or GOlang
  - think about algorithm on PiZero or separate PC

- understand and express geometric construct from dot shift to gradient data

- build algorithm to reconstruct wave surface, from gradient data
  - could also be very performance intensive, C++ or Go implementation my necessary

- design 3D-Case for Camera and PiZero
  - design rough PCB of PiZero and HQ Camera module
  - figure out orientation of PiZero to Camera, to create small usable package for Laser Application.

- (optional) incorporate Display, controls and/or LEDs
  - [2.0" 320x240 TFT Color](https://www.adafruit.com/product/4311]) ( 59.2mm x 35.5mm )
  - [1.3" 240x240 TFT Color + Joystick Add-on](https://www.adafruit.com/product/4506)  ( for zero designed - 65.5mm x 30.6mm )
  - [2.2" 320x240 TFT Color](https://www.adafruit.com/product/1480) ( 66.35mm x 40.63mm )

## Raspberry Pi HQ camera

|||
|---|---|
| Resolution |  12.3MP |
| col 2 is | centered |
| col 3 is | right-aligned |
(=4056x3040, sensor size 6.287mm x 4.712 mm )