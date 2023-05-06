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



class Encoder_Counter(Node):
    def __init__(self):
        
        
        super().__init__('Encoder_Counter')
        
        self.left_enc_prev=0
        self.right_enc_prev=0
        self.left_enc_new=0
        self.right_enc_new=0
        self.left_count=0
        self.right_count=0
        self.encoder_pub = self.create_publisher(Int32MultiArray, 'encoder_counts', 10)
        self.timer_ = self.create_timer(0.033, self.Pub_Counts)
        
        self.subscription = self.create_subscription(
            Int32MultiArray,
            '/left_encoder',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        numbers=msg.data
        print("Received Int32MultiArray: ", numbers)
        #self.get_logger().info(msg.data)

        
        
        #right_motor_enc_array=x
        '''
        self.left_enc_new=left_encoder[0]*2+left_encoder[1]
        #self.left_enc_new=x[2]*2+x[3]
        if(self.left_enc_prev==0):
            if(self.left_enc_new==1):
                self.left_count=self.left_count-1
            elif(self.left_enc_new==2):
                self.left_count=self.left_count+1
        elif(self.left_enc_prev==1):
            if(self.left_enc_new==3):
                self.left_count=self.left_count-1
            elif(self.left_enc_new==0):
                self.left_count=self.left_count+1
        elif(self.left_enc_prev==2):
            if(self.left_enc_new==0):
                self.left_count=self.left_count-1
            elif(self.left_enc_new==3):
                self.left_count=self.left_count+1
        elif(self.left_enc_prev==3):
            if(self.left_enc_new==2):
                self.left_count=self.left_count-1
            elif(self.left_enc_new==1):
                self.left_count=self.left_count+1

        if(self.right_enc_prev==0):
            if(self.right_enc_new==1):
                self.right_count=self.right_count-1
            elif(self.right_enc_new==2):
                self.right_count=self.right_count+1
        elif(self.right_enc_prev==1):
            if(self.right_enc_new==3):
                self.right_count=self.right_count-1
            elif(self.right_enc_new==0):
                self.right_count=self.right_count+1
        elif(self.right_enc_prev==2):
            if(self.right_enc_new==0):
                self.right_count=self.right_count-1
            elif(self.right_enc_new==3):
                self.right_count=self.right_count+1
        elif(self.right_enc_prev==3):
            if(self.right_enc_new==2):
                self.right_count=self.right_count-1
            elif(self.right_enc_new==1):
                self.right_count=self.right_count+1
        self.left_enc_prev=self.left_enc_new
        self.right_enc_prev=self.right_enc_new  
        '''
    

    def Pub_Counts(self):
        value=Int32MultiArray
        value=[self.left_count,self.right_count]
        self.encoder_pub.publish(Int32MultiArray(data=value)) 


        
    #def BiConvert(num):
    #    return num[0]*2+num[1]
    #def __del__(self):
    #    self.chip.__del__()
    
    
    
    

       

def main(args=None):
    rclpy.init(args=args)
    gpio_publisher = Encoder_Counter()
    rclpy.spin(gpio_publisher)
    gpio_publisher.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
