from time import sleep

from window import Window
from mpu6050 import MPU6050
from estimator import Estimator
from video import VideoPlayer

from PySide2.QtCore import QThread, Signal, QRect
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow

import os
import sys

class IMUThread(QThread):
    update_signal = Signal(dict)

    def __init__(self, imu, estimator, dt):
        super().__init__()
        self.mpu6050 = imu
        self.estimator = estimator
        self.dt = dt

        # run one time to initialize the vars
        p, q, r = self.mpu6050.read_gyro()
        x, y, z = self.mpu6050.read_accel()
        theta, phi = self.estimator.run(p, q, r , x, y, z, self.dt)   

        self.running = True
        
    def run(self):
        while self.running:
            # Read data from the IMU sensor
            p, q, r = self.mpu6050.read_gyro()
            x, y, z = self.mpu6050.read_accel()
            theta, phi = self.estimator.run(p, q, r , x, y, z, self.dt)
            gyro_data = {"theta": theta, "phi": phi}

            self.update_signal.emit(gyro_data)
            sleep(self.dt)  # Adjust the sleep time based on your application needs

    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(QRect(0, 0, 640, 480))

def main():
    i2c_bus = int(os.getenv('MPU_I2C_BUS', 3))  # Default to 3 if not set
    device_address = int(os.getenv('MPU_DEVICE_ADDRESS', '0x69'), 16)  # Default to 0x69 if not set

    mpu = MPU6050(i2c_bus, device_address)
    est = Estimator()
    app = QApplication(sys.argv)

    mw = MainWindow()
    win = Window()
    video = VideoPlayer()

    video.setParent(mw)
    win.setParent(mw)
    win.setGeometry(QRect(400, -50, 2000, 2000))
    video.setGeometry(QRect(0, 0, 1280, 720))

    dt = float(os.getenv('MPU_dt', 0.01))
    imu_thread = IMUThread(mpu, est, dt)
    imu_thread.update_signal.connect(win.update)
    imu_thread.start()

    mw.showFullScreen()
    app.exec_()

main()
