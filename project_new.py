import face_recognition as face
import argparse
import cv2
import imutils
from imutils.video import VideoStream 
import time
import RPi.GPIO as GPIO
ap=argparse.ArgumentParser()
ap.add_argument("-d","--detection-method",type=str,default="cnn")
args=vars(ap.parse_args())

male_face_encodings=[ -7.85724148e-02,   1.14086471e-01 ,  2.41411962e-02 , -5.57959341e-02,
   4.12065610e-02 , -3.06916572e-02 ,  3.92438844e-03 , -1.06071874e-01,
   1.91977561e-01 , -8.14845860e-02 ,  2.50276864e-01 ,  1.48030743e-03,
  -1.29924700e-01 , -1.69515133e-01 ,  4.35803607e-02 ,  7.78865740e-02,
  -9.05592144e-02 , -1.22896172e-01 , -9.71442014e-02 , -5.66511489e-02,
  -1.36947939e-02 ,  6.71350062e-02 ,  8.55996087e-03 , -1.26769999e-03,
  -1.54072896e-01 , -3.88335258e-01 , -1.11319937e-01 , -1.11142419e-01,
  -3.39194573e-02 , -1.23074025e-01 ,  3.12962458e-02 ,  1.50244921e-01,
  -2.41355121e-01 , -3.02141234e-02 , -1.73960216e-02 ,  9.04124454e-02,
   1.19647628e-03 ,  3.86124700e-02 ,  1.78993523e-01 ,  1.37060568e-01,
  -1.59993902e-01 , -2.36288086e-02 , -8.27450305e-04 ,  2.98713982e-01,
   1.68095514e-01 , -3.47816534e-02 , -3.65457870e-02 , -1.69734471e-04,
   1.12587541e-01 , -1.64770767e-01 ,  5.65771498e-02 ,  1.27822772e-01,
   1.17969066e-01 ,  6.10995777e-02 ,  7.18328059e-02 , -9.94108468e-02,
   1.74544118e-02 ,  2.58596577e-02 , -2.70038277e-01 ,  2.66039353e-02,
   6.82892278e-03 , -1.75286680e-01 , -1.48694128e-01 , -1.61887910e-02,
   1.73893109e-01 ,  1.54547125e-01 , -7.50750080e-02 , -1.32949173e-01,
   1.68126926e-01 , -9.26242322e-02 ,  2.38984022e-02 ,  9.86462384e-02,
  -1.18869491e-01 , -1.78611502e-01 , -2.89241254e-01 ,  1.29128352e-01,
   3.32826048e-01 ,  9.03781950e-02 , -1.84548780e-01 ,  4.16007377e-02,
  -8.19867402e-02 , -5.29643297e-02 ,  3.55558060e-02 ,  5.67606539e-02,
  -6.85041994e-02 ,  5.96397258e-02 , -5.08634485e-02 ,  7.98426569e-02,
   1.24039374e-01 ,  4.40909155e-02 , -8.09803009e-02 ,  1.97357640e-01,
  -1.29615560e-01 ,  5.76869510e-02 ,  3.37176472e-02 , -1.82215101e-03,
  -6.66946843e-02 , -1.44566894e-02 , -1.02440335e-01 , -1.67815499e-02,
   7.42164627e-02 , -1.28962547e-01 , -4.40006852e-02 ,  9.88250896e-02,
  -1.71770856e-01 ,  1.56897038e-01 , 4.02935967e-02 , -3.08329482e-02,
   1.38217434e-02 ,  5.19702910e-03 , -7.12288171e-02 , -4.89207618e-02,
   1.21981934e-01 , -2.75114924e-01 ,  2.35914171e-01 ,  1.01113260e-01,
  -5.35448976e-02 ,  1.67782053e-01 ,  4.07673307e-02 ,  8.06854963e-02,
  -5.99644408e-02 , -4.27299663e-02 , -1.61670372e-01 ,-6.04565404e-02,
   6.52222782e-02 ,  3.46553400e-02 ,  3.67322303e-02 , -1.39877461e-02]
known_faces=[male_face_encodings]
matched=0
face_locations=[] //here
face_encodings=[]
face_names=[]
print("IR sensor..")
IR_PIN1=24
IR_PIN2=23
GPIO.setmode(GPIO.BCM) //here
GPIO.setup(IR_PIN1, GPIO.IN) //here
GPIO.setup(IR_PIN2, GPIO.IN)
servoPIN = 17
GPIO.setup(servoPIN, GPIO.OUT)   //here
p = GPIO.PWM(servoPIN, 50) 
p.start(0)

try:	
	while 1:
		while 1:				
			if not GPIO.input(IR_PIN1): #here
				break	
		print("Detected Object")
		print("Initializing Camera")
		input_video=VideoStream(src=0).start()
		
		while not GPIO.input(IR_PIN1): #here
			frame=input_video.read()
			print("Captured frame")
			print("please wait, while the image is being processed... ")
			frame=imutils.resize(frame,width=100)
			rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #converting to rgb colour space
			face_locations=face.face_locations(rgb_frame,model=args["detection_method"]) #returns 2d array of bounding cooridnates(boxes) of face using cnn detector
			face_encodings_list=face.face_encodings(rgb_frame,face_locations) # returns 128 dimension face encoding
			if len(face_encodings_list)==0:
				print("No Face detected")
				continue
			print("Face detected")
			face_names=[]
			for face_encoding in face_encodings_list:
				match=face.compare_faces(known_faces,face_encoding,tolerance=0.6)
				name=None
				if match[0]:
					print("Recognised");
					matched=1
					break
					'''name="Ravi"
					face_names.append(name)
					for (top,right,bottom,left), name in zip(face_locations,face_names):
						if not name:
							continue
						cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
						cv2.rectangle(frame,(left,bottom-25),(right,bottom),(0,0,255))
						font=cv2.FONT_HERSHEY_DUPLEX
						cv2.putText(frame,name,(left+6,bottom-6),font,0.5,(255,255,255),1)'''
				else:
					print("Not recognised")
			if matched==1:
				break
			#cv2.imshow('frame',frame)
			#if cv2.waitKey(1) & 0xFF==ord('q'):
			#	break
		#cv2.destroyAllWindows()
		input_video.stop()

		if matched==1:
			print("Access Granted")			
			p.ChangeDutyCycle(5)
			time.sleep(1)
			while 1:
				if (GPIO.input(IR_PIN1)) or (not GPIO.input(IR_PIN2)):
					break
			p.ChangeDutyCycle(1.5)
			time.sleep(1)
			p.stop()
		else:
			print("Object moved")			
						
				
except KeyboardInterrupt:
	p.ChangeDutyCycle(1.5)
	time.sleep(1)
	p.stop()
	GPIO.cleanup()
	print("Terminated Program")
