#! /usr/bin/env python3

import rclpy
import subprocess
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped
from rclpy.node import Node
from rclpy.qos import QoSProfile
from sensor_msgs.msg import Imu

class Passing(Node):


    def __init__(self):
        super().__init__('passing_node')
        qos = QoSProfile(depth=10)
        self.imu_status_sub = self.create_subscription(Imu, 'imu', self.imu_status_callback, qos)
        self.imu_status_sub = self.create_subscription(Odometry, 'odom', self.odom_status_callback, qos)
        self.imu_status_sub = self.create_subscription(Odometry, '/wheel/odometry', self.wheel_odom_status_callback, qos)
        self.timer = self.create_timer(0.05,self.timer_callback)

        self.current_imu_data = 0.0
        self.current_imu_accel_x =0.0
        self.current_imu_accel_y =0.0
        self.current_imu_accel_z =0.0
        self.current_imu_gyro_x =0.0
        self.current_imu_gyro_y =0.0
        self.current_imu_gyro_z =0.0

        self.current_odom_data = 0.0
        self.current_wheel_odom_data =0.0

        self.log_accel_x=[]
        self.log_accel_y=[]
        self.log_accel_z=[]
        self.log_gyro_x=[]
        self.log_gyro_y=[]
        self.log_gyro_z=[]
        self.log_odom =[]
        self.log_wheel_odom=[]

    def imu_status_callback(self, msg):
        self.current_imu_data = msg
        self.current_imu_accel_x = msg.linear_acceleration.x
        self.current_imu_accle_y = msg.linear_acceleration.y
        self.current_imu_accle_y = msg.linear_acceleration.z
        self.current_imu_gyro_x =msg.angular_velocity.x
        self.current_imu_gyro_y =msg.angular_velocity.y
        self.current_imu_gyro_z =msg.angular_velocity.z


    def odom_status_callback(self,msg):
        self.current_odom_data = msg
        
    def wheel_odom_status_callback(self,msg):
        self.current_wheel_odom_data = msg


    def save_to_file(self,data,filename):
       with open(filename, 'a') as file:  # 'a' 모드를 사용해 파일에 내용을 추가
            for item in data:
                file.write(str(item) + '\n')  # IMU 데이터를 문자열로 변환하여 저장

    def timer_callback(self):
        self.log_accel_x.append(self.current_imu_accel_x)
        self.log_accel_y.append(self.current_imu_accel_y)
        self.log_accel_z.append(self.current_imu_accel_z)
        self.log_gyro_x.append(self.current_imu_gyro_x)
        self.log_gyro_y.append(self.current_imu_gyro_y)
        self.log_gyro_z.append(self.current_imu_gyro_z)

        if len(self.log_accel_x) >= 1000:
            self.save_to_file(self.log_accel_x, 'imu_data_accel_x.txt')

        





def main(args=None):
    rclpy.init(args=args)
    passing = Passing()
    rclpy.spin(passing)
    passing.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

