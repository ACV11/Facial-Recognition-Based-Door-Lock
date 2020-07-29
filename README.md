# Facial-Recognition-Based-Door-Lock
Facial recognition based door lock with obstruction detection using Python and Raspberry pi

The modules that have been used for face recognition are OpenCV and Face Recognition. 

A simple webcam can be used. If a person's face encdoings is in the acceptable list, a door controlled by a servo motor accordingly
opens. 

Two IR sensors have also been used. The first IR sensor detects when a person comes close to the door, and only then the camera
turns on. This is a power saving feature. Once the person has crossed the doorframwe, the second IR sensor is triggered and the door 
closes. Hence if the person is standing in the doorframe, then the dor will not close.
