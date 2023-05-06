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



class Encoder_Calculator(Node):
    def __init__(self):
        
        
        super().__init__('Encoder_Calculator')
        
        
        self.encoder_pub = self.create_publisher(Int32MultiArray, 'encoder_counts_calc', 10)
        self.timer_ = self.create_timer(0.033, self.Pub_Counts)
        self.MAXRPM=10
        self.WHEELDIA=.1
        self.BASEWIDE=.35
        self.CPR=1500/(2*3.1415)
        self.left_count=0
        self.right_count=0
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/joy',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        #use joy to get speeds
        x=1

        
        
        
    

    def Pub_Counts(self):
        value=Int32MultiArray
        omega=3.1415 #rad/sec
        x_speed=1#m/s
        omega_linear=omega*self.BASEWIDE/2
        right_speed=omega_linear+x_speed
        left_speed=-omega_linear+x_speed
        right_omega=right_speed/(self.WHEELDIA/2)
        right_count_speed=right_omega*(self.CPR)
        left_omega=left_speed/(self.WHEELDIA/2)
        left_count_speed=left_omega*self.CPR
        self.right_count=self.right_count+right_count_speed*0.033#counts =counts+counts/second*loop time
        self.left_count=self.left_count+left_count_speed*0.033#counts =counts+counts/second*loop time
        value=[int(self.left_count),int(self.right_count)]
        self.encoder_pub.publish(Int32MultiArray(data=value)) 


        
    #def BiConvert(num):
    #    return num[0]*2+num[1]
    #def __del__(self):
    #    self.chip.__del__()
    
    
    
    

       

def main(args=None):
    rclpy.init(args=args)
    gpio_publisher = Encoder_Calculator()
    rclpy.spin(gpio_publisher)
    gpio_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
