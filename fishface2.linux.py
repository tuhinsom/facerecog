import cv2
import glob

faceDet = cv2.CascadeClassifier("/root/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier("/root/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier("/root/opencv/data/haarcascades/haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier("/root/opencv/data/haarcascades/haarcascade_frontalface_alt_tree.xml")

glob_dir = "/home/tuhin/workspace/python/facerecognition"
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotions

def detect_faces(emotion):
    files = glob.glob("sorted_set/{}/*" .format(emotion)) #Get list of all images with emotion

    filenumber = 0
    for f in files:
        frame = cv2.imread(f.replace('%20',' ')) #Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert image to grayscale
        #print(gray)
        #Detect face using 4 different classifiers
        
        #print(faceDet.load(glob_dir+'/'+f))
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        #Go over detected faces, stop at first detected face, return empty if no face.
        if len(face) == 1:
            facefeatures = face
        elif len(face_two) == 1:
            facefeatures = face_two
        elif len(face_three) == 1:
            facefeatures = face_three
        elif len(face_four) == 1:
            facefeatures = face_four
        else:
            facefeatures = ""
        #print(facefeatures)
        #Cut and save face
        for (x, y, w, h) in facefeatures: #get coordinates and size of rectangle containing face
            #print( "face found in file: {}".format(len(facefeatures)) )
            gray = gray[y:y+h, x:x+w] #Cut the frame to size
            
            try:
                out = cv2.resize(gray, (350, 350)) #Resize face so all images have same size
                cv2.imwrite("dataset/{}/{}.jpg" .format(emotion, filenumber), out) #Write image
            except:
               pass #If error, pass file
        filenumber += 1 #Increment image number
        
#print(emotions)
for emotion in emotions: 
    detect_faces(emotion) #Call functiona
