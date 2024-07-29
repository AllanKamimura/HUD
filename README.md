# HUD

A Heads-Up Display (HUD) is a camera overlay (an image draw over the image) that allows pilots to get navigation info without taking the eyes off the "road". 

This project implements an overlay drawn using QT, integrated with a 6050 MPU and running on a Toradex Apalis iMX8QM device.

# Demo
<video src="https://github.com/user-attachments/assets/2254ea5e-ee4a-4235-9195-d832db65c2a6" width="720" autoplay></video>






# Project

- [MPU Library](src/mpu6050.py)
- [Euler Angles estimator](src/estimator.py)
- [GStreamer Camera Capture](src/video.py)
- [QT Drawing](src/window.py)

## Camera support
<video src="https://github.com/user-attachments/assets/3a171a6b-d128-4473-93ac-e7736bf0bb58" width="720" controls autoplay></video>


[Onshape CAD Project](https://cad.onshape.com/documents/2a28808b03ecd87718e7eb28/w/81ed70e87d40cad4075aa8fc/e/4d436e70dbfc37b4c7834171?renderMode=0&uiState=66a78e585193994982861507)


# How to run

Connect the I²C MPU, I'm using an [Ixora Carrier Board](https://docs.toradex.com/114744-ixora-carrier-board-datasheet-v1.3.pdf).

```sh
docker compose --file mpu.yml up -d
```
