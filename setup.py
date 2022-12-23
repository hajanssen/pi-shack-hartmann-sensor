from setuptools import setup

setup(
    name='SHSlib',
    version='0.1.0',    
    description='A Libary for Processing Shak-hartman Images for wavefront reconstruction',
    url='https://github.com/hajanssen/pi-shack-hartmann-sensor',
    author='Hauke Janssen',
    author_email='haukejanssen6@web.de',
    license='BSD 2-clause',
    packages=['pyexample'],
    install_requires=['numpy','picamera'],
    )
