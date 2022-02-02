
import time

# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-06-21
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import os
import sys
import time
import spidev
import logging
import numpy as np

class RaspberryPi:
    def __init__(self,spi=spidev.SpiDev(0,0),spi_freq=40000000,rst = 27,dc = 25,bl = 18,bl_freq=1000,i2c=None,i2c_freq=100000):
        import RPi.GPIO      
        self.np=np
        self.RST_PIN= rst
        self.DC_PIN = dc
        self.BL_PIN = bl
        self.SPEED  =spi_freq
        self.BL_freq=bl_freq
        self.GPIO = RPi.GPIO
        #self.GPIO.cleanup()
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN,   self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN,    self.GPIO.OUT)
        self.GPIO.setup(self.BL_PIN,    self.GPIO.OUT)
        self.GPIO.output(self.BL_PIN,   self.GPIO.HIGH)        
        #Initialize SPI
        self.SPI = spi
        if self.SPI!=None :
            self.SPI.max_speed_hz = spi_freq
            self.SPI.mode = 0b00

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        if self.SPI!=None :
            self.SPI.writebytes(data)
    def bl_DutyCycle(self, duty):
        self._pwm.ChangeDutyCycle(duty)
        
    def bl_Frequency(self,freq):
        self._pwm.ChangeFrequency(freq)
           
    def module_init(self):
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DC_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.BL_PIN, self.GPIO.OUT)
        self._pwm=self.GPIO.PWM(self.BL_PIN,self.BL_freq)
        self._pwm.start(100)
        if self.SPI!=None :
            self.SPI.max_speed_hz = self.SPEED        
            self.SPI.mode = 0b00     
        return 0

    def module_exit(self):
        logging.debug("spi end")
        if self.SPI!=None :
            self.SPI.close()
        
        logging.debug("gpio cleanup...")
        self.GPIO.output(self.RST_PIN, 1)
        self.GPIO.output(self.DC_PIN, 0)        
        self._pwm.stop()
        time.sleep(0.001)
        self.GPIO.output(self.BL_PIN, 1)
        #self.GPIO.cleanup()


'''
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
'''

### END OF FILE ###



class LCD(RaspberryPi):

    width = 240
    height = 320 
    def command(self, cmd):
        self.digital_write(self.DC_PIN, self.GPIO.LOW)
        self.spi_writebyte([cmd])

    def data(self, val):
        self.digital_write(self.DC_PIN, self.GPIO.HIGH)
        self.spi_writebyte([val])
    def reset(self):
        """Reset the display"""
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.LOW)
        time.sleep(0.01)
        self.GPIO.output(self.RST_PIN,self.GPIO.HIGH)
        time.sleep(0.01)
        
    def Init(self):
        """Initialize dispaly"""  
        self.module_init()
        self.reset()

        self.command(0x11);'''Sleep out'''
	
        self.command(0xCF);
        self.data(0x00);
        self.data(0xC1);
        self.data(0X30);
        self.command(0xED);
        self.data(0x64);
        self.data(0x03);
        self.data(0X12);
        self.data(0X81);
        self.command(0xE8);
        self.data(0x85);
        self.data(0x00);
        self.data(0x79);
        self.command(0xCB);
        self.data(0x39);
        self.data(0x2C);
        self.data(0x00);
        self.data(0x34);
        self.data(0x02);
        self.command(0xF7);
        self.data(0x20);
        self.command(0xEA);
        self.data(0x00);
        self.data(0x00);
        self.command(0xC0);'''Power control'''
        self.data(0x1D);'''VRH[5:0]'''
        self.command(0xC1);'''Power control'''
        self.data(0x12);'''SAP[2:0];BT[3:0]'''
        self.command(0xC5);'''VCM control'''
        self.data(0x33);
        self.data(0x3F);
        self.command(0xC7);'''VCM control'''
        self.data(0x92);
        self.command(0x3A);'''Memory Access Control'''
        self.data(0x55);
        self.command(0x36);'''Memory Access Control'''
        self.data(0x08);
        self.command(0xB1);
        self.data(0x00);
        self.data(0x12);
        self.command(0xB6);'''Display Function Control'''
        self.data(0x0A);
        self.data(0xA2);

        self.command(0x44);
        self.data(0x02);

        self.command(0xF2);'''3Gamma Function Disable'''
        self.data(0x00);
        self.command(0x26);'''Gamma curve selected'''
        self.data(0x01);
        self.command(0xE0);'''Set Gamma'''
        self.data(0x0F);
        self.data(0x22);
        self.data(0x1C);
        self.data(0x1B);
        self.data(0x08);
        self.data(0x0F);
        self.data(0x48);
        self.data(0xB8);
        self.data(0x34);
        self.data(0x05);
        self.data(0x0C);
        self.data(0x09);
        self.data(0x0F);
        self.data(0x07);
        self.data(0x00);
        self.command(0XE1);'''Set Gamma'''
        self.data(0x00);
        self.data(0x23);
        self.data(0x24);
        self.data(0x07);
        self.data(0x10);
        self.data(0x07);
        self.data(0x38);
        self.data(0x47);
        self.data(0x4B);
        self.data(0x0A);
        self.data(0x13);
        self.data(0x06);
        self.data(0x30);
        self.data(0x38);
        self.data(0x0F);
        self.command(0x29);'''Display on'''

  
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(0x2A)
        self.data(Xstart>>8)        #Set the horizontal starting point to the high octet
        self.data(Xstart & 0xff)    #Set the horizontal starting point to the low octet
        self.data(Xend>>8)          #Set the horizontal end to the high octet
        self.data((Xend - 1) & 0xff)#Set the horizontal end to the low octet 

        #set the Y coordinates
        self.command(0x2B)
        self.data(Ystart>>8)
        self.data((Ystart & 0xff))
        self.data(Yend>>8)
        self.data((Yend - 1) & 0xff )

        self.command(0x2C)    
        
    def ShowImage(self,Image,Xstart=0,Ystart=0):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth == self.height and imheight ==  self.width:
            img = self.np.asarray(Image)
            pix = self.np.zeros((self.width, self.height,2), dtype = self.np.uint8)
            #RGB888 >> RGB565
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x78) 
            self.SetWindows ( 0, 0, self.height,self.width)
            self.digital_write(self.DC_PIN,self.GPIO.HIGH)
            for i in range(0,len(pix),4096):
                self.spi_writebyte(pix[i:i+4096])
            
        else :
            img = self.np.asarray(Image)
            pix = self.np.zeros((imheight,imwidth , 2), dtype = self.np.uint8)
            
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))

            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x08) 
            self.SetWindows ( 0, 0, self.width, self.height)
            self.digital_write(self.DC_PIN,self.GPIO.HIGH)
            for i in range(0,len(pix),4096):
                self.spi_writebyte(pix[i:i+4096])		
                
    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,self.GPIO.HIGH)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	
        
