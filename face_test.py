import face_recognition
import picamera
import pickle
import numpy as np
print('library imported')
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype = np.uint8)

my_face = face_recognition.load_image_file("rob_face.jpg")
my_face_enc = face_recognition.face_encodings(my_face)[0]
#my_face_enc2 = pickle.load(open('face.pkl', 'rb'))
#print(type(my_face_enc), type(my_face_enc2))
face_locations = []
face_encodings = []

print('starting')
while True:
	camera.capture(output, format="rgb")
	face_locations = face_recognition.face_locations(output)
	print("found {} faces!".format(len(face_locations)))

	face_encodings = face_recognition.face_encodings(output, face_locations)
	
	for face in face_encodings:
		match = face_recognition.compare_faces([my_face_enc], face)
		name = "Unknown"
		if match[0]:
			name = "Rob"
		print("found {}!".format(name))


