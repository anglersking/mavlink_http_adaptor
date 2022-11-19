#!/usr/bin/env python
# -*- coding: utf-8-*-
"""© Copyright2015-2016, 3D Robotics.simple_goto.py:GUIDED mode "simple goto" example (Copter Only)Demonstrates how toarm and takeoff in Copter and how to navigate to points usingVehicle.simple_goto.
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

class Pixhawk:
    def __init__(self,uart_device,wait_ready,baud):
        self.uart_device=uart_device
        self.wait_ready = wait_ready
        self.baud=baud
        self.vehicle=self.com_connect()

    def com_connect(self):
        print('Connectingto vehicle on: %s' % self.uart_device)
        vehicle = connect(self.uart_device, wait_ready=self.wait_ready, baud=self.baud)
        vehicle.armed = False
        return vehicle

    def arm(self):
        self.vehicle.arm=True

    def armchecks(self):
        print("Basic pre-armchecks")
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle toinitialise...")

            time.sleep(1)
    def check_is_arming(self):
        while not self.vehicle.armed:
            print(" Waiting forarming...")
            time.sleep(1)
    def take_off(self,Target_Altitude=10):
        print("Taking off!")
        self. vehicle.simple_takeoff(Target_Altitude)

    def To_Target_Altitude(self,Target_Altitude):
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
            # vehicle.location.global_relative_frame.alt为相对于home点的高度
            if self.vehicle.location.global_relative_frame.alt >= Target_Altitude * 0.95:
                print("Reached targetaltitude")
                break
            # 等待1s
            time.sleep(1)

    def log_info(self):
        print("log_info")
        print("Autopilot Firmware version: %s" % self.vehicle.version)
        print("Autopilot capabilities (supports ftp): %s" % self.vehicle.capabilities.ftp)
        print("Global Location: %s" % self.vehicle.location.global_frame)
        print("Global Location (relative altitude): %s" % self.vehicle.location.global_relative_frame)
        print("Local Location: %s" % self.vehicle.location.local_frame)  # NED
        print("Attitude: %s" % self.vehicle.attitude)
        print("Velocity: %s" % self.vehicle.velocity)
        print("GPS: %s" % self.vehicle.gps_0)
        print("Groundspeed: %s" % self.vehicle.groundspeed)
        print("Airspeed: %s" % self.vehicle.airspeed)
        print("Gimbal status: %s" % self.vehicle.gimbal)
        print("Battery: %s" % self.vehicle.battery)
        print("EKF OK?: %s" % self.vehicle.ekf_ok)
        print("Last Heartbeat: %s" % self.vehicle.last_heartbeat)
        print("Rangefinder: %s" % self.vehicle.rangefinder)
        print("Rangefinder distance: %s" % self.vehicle.rangefinder.distance)
        print("Rangefinder voltage: %s" % self.vehicle.rangefinder.voltage)
        print("Heading: %s" % self.vehicle.heading)
        print("Is Armable?: %s" % self.vehicle.is_armable)
        print("System status: %s" % self.vehicle.system_status.state)
        print("Mode: %s" % self.vehicle.mode.name)  # settable
        print("Armed: %s" % self.vehicle.armed)  # settable
    def set_air_speed(self,air_speed):
        print("Setdefault/target airspeed {0}".format(air_speed))

        # vehicle.airspeed变量可读可写，且读、写时的含义不同。
        # 读取时，为无人机的当前空速；写入时，设定无人机在执行航点任务时的默认速度
        self.vehicle.airspeed = air_speed

    def create_point(self,latitude,longitude,home_artitude):
        point=LocationGlobalRelative(latitude,longitude , home_artitude)
        return point

    def retu_launch(self):
        print("Returningto Launch")
        self.vehicle.mode = VehicleMode("RTL")

    def to_point(self,latitude,longitude,sleep_time):
        self.vehicle.simple_goto(self.create_point(latitude,longitude))
        time.sleep(sleep_time)  # 发送指令，让无人机前往第二个航点
        print("Goingtowards second point for {0} seconds (groundspeed set to 10 m/s) ...".format(sleep_time))

    def delet_obj(self):
        # 退出之前，清除vehicle对象
        print("Closevehicle object")
        self.vehicle.close()

    def send_ned_velocity(self,velocity_x, velocity_y, velocity_z, duration):
        """
        Move vehicle in direction based on specified velocity vectors.
        """
        msg = self.vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111,
            0, 0, 0,
            velocity_x, velocity_y, velocity_z,
            0, 0, 0,
            0, 0)
        # 循环发送几次
        for x in range(0, duration):
            # 发送指令
            self.vehicle.send_mavlink(msg)
            time.sleep(1)

    # 偏航
    def condition_yaw(self,heading, relative=False):
        if relative:
            is_relative = 1
        else:
            is_relative = 0
        msg = self.vehicle.message_factory.command_long_encode(
            0, 0,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,
            heading,
            0,
            1,
            is_relative,
            0, 0, 0)
        # 发送指令
        self.vehicle.send_mavlink(msg)


    def arm_and_takeoff(self,Mode="GUIDED",Target_Altitude=10):
        print("Basic pre-armchecks")
        self.armchecks()
        print("Arming motors")
        self.arm()

        self.vehicle.mode = VehicleMode(Mode)
        # 通过设置vehicle.armed状态变量为True，解锁无人机
        self.vehicle.armed = True
        self.check_is_arming()
        self.take_off(Target_Altitude)
        self.To_Target_Altitude(Target_Altitude)