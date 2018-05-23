from PIL import Image
import picamera
import face_recognition
import numpy as np
import pickle
import time
import os

class FaceController(object):
	def __init__(self, camera):
		print("libs loaded")	
		self.camera = camera
		self.camera.resolution = (320, 240)
		self.face_enc = pickle.load(open('/home/pi/Droid/face.pkl', 'rb'))		
		self.output = np.empty((240, 320, 3), dtype=np.uint8)
		print("done with init")

	def scan_for_faces(self):
		face_locations = []
		face_encodings = []

		self.camera.start_preview()
		count = 0
		while count < 5:
			count += 1	
			time.sleep(1)
			print("taking pic...")
			self.camera.capture(self.output, format="rgb")	
			print("done with pic")		
			face_locations = face_recognition.face_locations(self.output)
			print("found {} faces!".format(len(face_locations)))
			face_encodings = face_recognition.face_encodings(self.output, face_locations)
			for face in face_encodings:
				match = face_recognition.compare_faces([x[1] for x in self.face_enc], face)
				name = ""
				for i in range(len(match)):
					if match[i]:
						name = name + self.face_enc[i][0] + " "
				if name != "":		
					print("found {}!".format(name))
					self.camera.stop_preview()
					return name
		self.camera.stop_preview()
	
	def create_pkl(self):
		face_imgs = [i for i in os.listdir('/home/pi/Droid') if i.split('.')[-1] == 'jpg']
			
		faces = [(f.split('_')[0], face_recognition.load_image_file(f)) for f in face_imgs]
		face_enc = []
		for name, f in faces:
			face_enc.append((name, face_recognition.face_encodings(f)[0]))
		pickle.dump(face_enc, open('face.pkl', 'wb'))


if __name__ == "__main__":
	cam = picamera.PiCamera()
	fc = FaceController(cam)
	fc.create_pkl()
