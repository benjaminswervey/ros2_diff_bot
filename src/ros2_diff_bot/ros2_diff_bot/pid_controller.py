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
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32MultiArray



class pid_controller(Node):
    def __init__(self):
        
        
        super().__init__('pid_controller')
        self.p=0.1
        self.i=0.1
        self.d=0.1

        self.pwm_right=0.0
        self.pwm_left=0.0

        self.calc_counts_left=0.0
        self.calc_counts_right=0.0
        
        self.counts_right=0.0
        self.counts_left=0.0

        self.calc_recieved=False

        self.previous_error_right=0.0
        self.previous_error_left=0.0

        self.error_right=0.0
        self.error_left=0.0

        self.cum_error_right=0.0
        self.cum_error_left=0.0

        self.encoder_pub = self.create_publisher(Float32MultiArray, 'pwm', 10)

        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/encoder_counts',
            self.listener_callback_real,
            10)
        self.subscription

        self.subscription2 = self.create_subscription(
            Int32MultiArray,
            '/encoder_counts_calc',
            self.listener_callback_calc,
            10)
        self.subscription2  # prevent unused variable warning

    def listener_callback_calc(self, msg):
        self.calc_recieved=True
        x=msg.data
        self.calc_counts_left=x[0]
        self.calc_counts_right=x[1]
        


    def listener_callback_real(self, msg):
        x=msg.data

        self.counts_left=x[0]
        self.counts_right=x[1]
        
        if(self.calc_recieved==True):
            self.error_left=self.counts_left-self.calc_counts_left
            self.error_right=self.counts_right-self.calc_counts_right

            self.previous_error_left=self.error_left
            self.previous_error_right=self.error_right

            self.calc_recieved=False

            diff_error_right=self.error_right-self.previous_error_right
            diff_error_left=self.error_left-self.previous_error_left

            self.cum_error_left=self.cum_error_left+self.error_left
            self.cum_error_right=self.cum_error_right+self.error_right
            print("Received Int32MultiArray errorleft: ", self.error_left)
            self.pwm_left=self.error_left*self.p+diff_error_left*self.d+self.cum_error_left*self.i
            self.pwm_right=self.error_right*self.p+diff_error_right*self.d+self.cum_error_right*self.i
            value=[(self.pwm_left),(self.pwm_right)]
            self.encoder_pub.publish(Float32MultiArray(data=value)) 





        
    

    def Pub_Counts(self):
        y=1


        
    #def BiConvert(num):
    #    return num[0]*2+num[1]
    #def __del__(self):
    #    self.chip.__del__()
    
    
    
    

       

def main(args=None):
    rclpy.init(args=args)
    gpio_publisher = pid_controller()
    rclpy.spin(gpio_publisher)
    gpio_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
