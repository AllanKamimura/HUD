# HUD

A Heads-Up Display (HUD) is a camera overlay (an image draw over the image) that allows pilots to get navigation info without taking the eyes off the "road". 

This project implements an overlay drawn using QT, integrated with a 6050 MPU and running on a Toradex Apalis iMX8QM device.

# Demo
<video width="640" height="480" controls>
  <source src="./assets/demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


# Project

- [MPU Library](src/mpu6050.py)
- [Euler Angles estimator](src/estimator.py)
- [GStreamer Camera Capture](src/video.py)
- [QT Drawing](src/window.py)

## Camera support
<video width="640" height="480" controls>
  <source src="./assets/camera_support.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


[Onshape CAD Project](https://cad.onshape.com/documents/2a28808b03ecd87718e7eb28/w/81ed70e87d40cad4075aa8fc/e/4d436e70dbfc37b4c7834171?renderMode=0&uiState=66a78e585193994982861507)


# How to run

Connect the I²C MPU, I'm using an [Ixora Carrier Board](https://docs.toradex.com/114744-ixora-carrier-board-datasheet-v1.3.pdf).

```sh
docker compose --file mpu.yml up -d
```
