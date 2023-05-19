# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
import gpiod
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray


class Encoder_Reader(Node):
    def __init__(self):
        
        
        super().__init__('encoder_reader')
        
        Chip0=gpiod.chip(0)#Motor 1, Encoder 2, Pin 5 = chip 0, line 4, (Yellow Wire)
        Chip1 = gpiod.chip(1)#Motor 1, Encoder 1, Pin 7 = chip 0, line 6, (Green Wire)
        #M2E1=gpiod.chip(0)#Motor 2, Encoder 1, Pin 16  = chip 1, line 93 (Green Wire)
        #M2E2 = gpiod.chip(1)#Motor 2, Encoder 2, Pin 18  = chip 1, line 94 (Yellow Wire)
        
        self.M1E1_Line = Chip0.get_line(4)
        self.M1E2_Line=Chip1.get_line(98)
        self.M2E1_Line = Chip1.get_line(93)
        self.M2E2_Line=Chip1.get_line(94)
        '''
        self.left_test_1=0
        self.left_test_2=0
        self.right_test_1=0
        self.right_test_2=0
        self.count=0
        '''
        self.M1E1_config=gpiod.line_request()
        self.M1E2_config=gpiod.line_request()
        self.M2E1_config=gpiod.line_request()
        self.M2E2_config=gpiod.line_request()

        self.M1E1_config.consumer="encoder_reader"
        self.M1E2_config.consumer="encoder_reader"
        self.M2E1_config.consumer="encoder_reader"
        self.M2E2_config.consumer="encoder_reader"

        self.M1E1_config.request_type=gpiod.line_request.DIRECTION_INPUT
        self.M1E2_config.request_type=gpiod.line_request.DIRECTION_INPUT
        self.M2E1_config.request_type=gpiod.line_request.DIRECTION_INPUT
        self.M2E2_config.request_type=gpiod.line_request.DIRECTION_INPUT

        self.M1E1_Line.request(self.M1E1_config)
        self.M1E2_Line.request(self.M1E2_config)
        self.M2E1_Line.request(self.M2E1_config)
        self.M2E2_Line.request(self.M2E2_config)
        
        self.left_encoder_pub = self.create_publisher(Int32MultiArray, 'left_encoder', 10)
        self.right_encoder_pub = self.create_publisher(Int32MultiArray, 'right_encoder', 10)

        #self.timer_ = self.create_timer(0.1, self.read_encoder)
        self.timer_ = self.create_timer(0.1, self.encoder_test)

    def encoder_test(self):
       '''
       self.left_test_1=(self.left_test_1+1)%2
       self.left_test_2=(self.left_test_1+1)%2
       self.right_test_1=(self.left_test_1+1)%2
       self.right_test_2=(self.left_test_1+1)%2
       '''

       
       
       
       

       left=Int32MultiArray()
       left.data=[self.M1E1_Line.get_value(),self.M1E2_Line.get_value()]
        
       right=Int32MultiArray()
       right.data=[self.M2E1_Line.get_value(),self.M2E2_Line.get_value()]
        
       self.left_encoder_pub.publish(left)
       self.right_encoder_pub.publish(right)

        
    def read_encoder(self):
        right=Int32MultiArray()
        right.data=[self.M1E1_Line.get_value(),self.M1E2_Line.get_value()]
        
        left=Int32MultiArray()
        left.data=[self.M2E1_Line.get_value(),self.M2E2_Line.get_value()]
        
        self.left_encoder_pub.publish(left)
        self.right_encoder_pub.publish(right)
        

    #def __del__(self):
    #    self.chip.__del__()
    
    
    
    

       

def main(args=None):
    rclpy.init(args=args)
    gpio_publisher = Encoder_Reader()
    rclpy.spin(gpio_publisher)
    gpio_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
