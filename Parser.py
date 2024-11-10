#Webcam parser script V1.0.0 - RF and DD

#System Dependencies
import os
import sqlite3

#ROS2 Dependencies
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
from rclpy.time import Time

#Import OpenCV
import cv2

#Parsing Dependencies
import numpy as np

#Parser Class
class Parser():
    #Initialization function - runs on object creation
    def __init__(self, path, debug = True):
        self.debug = debug
        
        if (self.debug == True):
            print("Initializing parser object")

        #Initialize lists and dataframes for later storage
        self.abs_paths = []
        
        self.connections = []
        self.fileCursors = []
        
        self.data = []
        self.topic_types = []
        self.topic_ids = []
        self.topic_messages = []

        #Initialize variables for status counts to 0 
        self.fail_count = 0
        self.db_count = 0

        self.image_dir = path + "/proc/"
        os.makedirs(self.image_dir, exist_ok = True)

        #Use walk to get root dir, and files
        for (root, dirs, files) in os.walk(path, topdown = True):
            #Iterate through (sorted) list of files
            dirs.sort()

            print(files)
            
            for file in sorted(files):
                print(file)
                #If file is of the appropriate type
                if ".db3" in file:
                    #Calculate absolute path
                    self.abs_paths.append(os.path.join(root, file))

                    #Try to connect to database and retrieve metadata per topic
                    try:
                        self.connections.append(sqlite3.connect(self.abs_paths[-1]))
                        self.fileCursors.append(self.connections[-1].cursor())

                        self.data.append(self.fileCursors[-1].execute("SELECT id, name, type FROM topics").fetchall())

                    #If this fails, increment the fail counter
                    except:
                        self.fail_count = self.fail_count + 1

                        if (self.debug == True):
                            print("Error: Couldn't load " + str(file))

                    #Otherwise finish loading, generate UUID and increment db number
                    else:
                        self.topic_types.append({name_of:type_of for id_of, name_of, type_of in self.data[-1]})
                        self.topic_ids.append({name_of:id_of for id_of, name_of, type_of in self.data[-1]})
                        self.topic_messages.append({name_of:get_message(type_of) for id_of, name_of, type_of in self.data[-1]})
                        
                        self.db_count += 1
                        
                        if (self.debug == True):
                            print("Loaded " + str(file))

    #Destructor function - runs on object destruction
    def __del__(self):
        if (self.debug == True):
            print("Destroying parser object")

        #Iterate through all open databases, ensure they are closed
        for it in range(0, self.db_count):
            try:
                #If connection isn't open, do nothing
                if (self.connections[it] is None):
                    pass

                #If connection is open, close it
                else:
                    self.connections[it].close()

            except:
                pass

    def parse_all(self):
        for i in range(0, self.db_count):
            self.__convert_webcam_to_png(i)

                
    #__get_messages - Gets messages from
    def __get_messages(self, topic_name, it):
        try:
            topic_id = self.topic_ids[it][topic_name]

        except:
            return False

        else:
            rows = self.fileCursors[it].execute("SELECT timestamp, data FROM messages WHERE topic_id = {}".format(topic_id)).fetchall()
            return [(deserialize_message(data, self.topic_messages[it][topic_name])) for timestamp, data in rows]
        
    
    def __convert_webcam_to_png(self, it):
        raw_messages = self.__get_messages("/camera/camera/color/image_raw", it)

        if raw_messages is False:
            return False

        i = 0

        for message in raw_messages:
            # Convert data to a numpy array with the specified shape
            try:
                img_data = np.array(message.data, dtype=np.uint8)
                img = img_data.reshape((message.height, message.width, 3))  # 3 channels for RGB

                # Save the image
                cv2.imwrite(f"{self.image_dir}pic{i}.png", img)
                i += 1
            except Exception as e:
                print(f"Warning: Decoding image data failed due to {e}")
                continue  # Skip this iteration if decoding fails

        return True


if __name__ == "__main__":
    P00 = Parser("./rosbag_sensors_1969-12-31_20-50-50.bag")
    P00.parse_all()