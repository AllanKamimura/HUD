import smbus2
import time
import numpy as np

class MPU6050(object):
    # Details about MPU6050 registers are available at https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

    # Registers
    ## MPU6050 sample rate register
    SMPLRT_DIV = 0x19

    ## MPU6050 configuration registers
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    ACELL_CONFIG = 0x1C

    ## MPU6050 data registers
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    TEMP_OUT_H   = 0x41 # Temperature in degrees C = (TEMP_OUT Register Value as a signed quantity)/340 + 36.53
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    ## MPU6050 power management register
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    # CONFIG values
    ## Frame Synchronization (FSYNC) and  Digital Low Pass Filter (DLPF) 
    DLPF_DISABLE= 0x07
    DLPF_5_HZ   = 0x06
    DLPF_10_HZ  = 0x05
    DLPF_21_HZ  = 0x04
    DLPF_44_HZ  = 0x03
    DLPF_94_HZ  = 0x02
    DLPF_184_HZ = 0x01
    DLPF_260_HZ = 0x00

    ## SMPLRT_DIV values 
    ### SAMPLERATE = x / (D*), where x = 1 if (DLPF_DISABLE or DLPF_260_HZ) else x = 8
    SAMPLERATE_D1_HZ = 0X00
    SAMPLERATE_D2_HZ = 0X01
    SAMPLERATE_D3_HZ = 0X02
    SAMPLERATE_D4_HZ = 0X03
    SAMPLERATE_D5_HZ = 0X04
    SAMPLERATE_D6_HZ = 0X05
    SAMPLERATE_D7_HZ = 0X06
    SAMPLERATE_D8_HZ = 0X07

    ## GYRO_CONFIG values
    RANGE_250_DEG  = 0x00 # +/-  250 deg/s
    RANGE_500_DEG  = 0x08 # +/-  500 deg/s (default)
    RANGE_1000_DEG = 0x10 # +/- 1000 deg/s
    RANGE_2000_DEG = 0x18 # +/- 2000 deg/s

    ## ACCEL_CONFIG values
    RANGE_2_G    = 0x00  # +/-  2g (default)
    RANGE_4_G    = 0x08  # +/-  4g
    RANGE_8_G    = 0x10  # +/-  8g
    RANGE_16_G   = 0x18  # +/- 16g

    ACC_LSB = {
        RANGE_2_G : 16384,
        RANGE_4_G : 8192,
        RANGE_8_G : 4096,
        RANGE_16_G: 2048,
        }

    GYRO_LSB = {
           RANGE_250_DEG : 131,
           RANGE_500_DEG : 65.5,
           RANGE_1000_DEG: 32.8,
           RANGE_2000_DEG: 16.4,
           }
    
    def __init__(self, bus = 1, device_address = 0x68):
        # SETUP
        self.accel_range = self.RANGE_16_G
        self.gyro_range  = self.RANGE_2000_DEG
        self.sample_rate = self.SAMPLERATE_D8_HZ
        self.dlpf        = self.DLPF_5_HZ

        # LSB
        self.acc_lsb  = self.ACC_LSB[self.accel_range]
        self.gyro_lsb = self.GYRO_LSB[self.gyro_range]

        # Initial configuration for the MPU6050
        self.bus = smbus2.SMBus(bus)
        self.device_address = device_address

        # Select the internal oscillator (8MHz) as clock source
        self.bus.write_byte_data(self.device_address, self.PWR_MGMT_1, 0x00)

        self.bus.write_byte_data(self.device_address, self.CONFIG      , self.dlpf)
        self.bus.write_byte_data(self.device_address, self.SMPLRT_DIV  , self.sample_rate)
        self.bus.write_byte_data(self.device_address, self.GYRO_CONFIG , self.gyro_range )
        self.bus.write_byte_data(self.device_address, self.ACELL_CONFIG, self.accel_range)

    def read_register(self, register_addres):
        # Masurements values are 16-bit
        high = self.bus.read_byte_data(self.device_address, register_addres    )
        low  = self.bus.read_byte_data(self.device_address, register_addres + 1) 

        # Convert the 8-bit values into a 16-bit value
        value = ((high << 8) | low)
        
        # Convert to 16-bit 2’s complement value
        if value & (1 << 15):
            value = value - (1 << 16)

        return value

    def read_accel(self):
        X = self.read_register(self.ACCEL_XOUT_H) / self.acc_lsb
        Y = self.read_register(self.ACCEL_YOUT_H) / self.acc_lsb
        Z = self.read_register(self.ACCEL_ZOUT_H) / self.acc_lsb

        return X,Y,Z
    
    def read_gyro(self):
        P = self.read_register(self.GYRO_XOUT_H) / self.gyro_lsb
        Q = self.read_register(self.GYRO_YOUT_H) / self.gyro_lsb
        R = self.read_register(self.GYRO_ZOUT_H) / self.gyro_lsb

        return P,Q,R
