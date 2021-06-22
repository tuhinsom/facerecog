import cv2
import glob
import random
import numpy as np
import pickle

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list
#fishface = cv2.createFisherFaceRecognizer() #Initialize fisher face classifier
fishface = cv2.face.FisherFaceRecognizer_create()

model_filename = 'emotion_recognizer_model.yml'
data = {}

def get_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("dataset/{}/*" .format(emotion))
    #print(files)
    random.shuffle(files)
    
    training = files[:int(len(files)*0.8)] #get first 80% of file list
    prediction = files[-int(len(files)*0.2):] #get last 20% of file list
    return training, prediction

def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        #print(emotion)
        #print(prediction)
        #Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(emotions.index(emotion))
    
        for item in prediction: #repeat above process for prediction set
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
            prediction_labels.append(emotions.index(emotion))
    #print(prediction_data)
    return training_data, training_labels, prediction_data, prediction_labels

def run_recognizer():
    training_data, training_labels, prediction_data, prediction_labels = make_sets()
    
    
    """fishface.train(training_data, np.asarray(training_labels))"""
    print ("training fisher face classifier")
    print ("size of training set is:{} images" .format( len(training_labels) ))
    fishface.read(model_filename)
    print ("predicting classification set")
    
    cnt = 0
    correct = 0
    incorrect = 0
    for image in prediction_data:
        pred, conf = fishface.predict(image)
        print(prediction_labels[pred])
        print("\n")
        if pred == prediction_labels[cnt]:
            correct += 1
            cnt += 1
        else:
            incorrect += 1
            cnt += 1
    return ((100*correct)/(correct + incorrect))
	
def create_emotion_recognizer(counter):
    training_data, training_labels, prediction_data, prediction_labels = make_sets()
    
    print ("training fisher face classifier")
    print ("size of training set is:{} images" .format( len(training_labels) ))
    
    fishface.train(training_data, np.asarray(training_labels))

    
    

#Now run it
metascore = []
exec_flag = 2

if exec_flag == 1:
    for i in range(0,10):
        create_emotion_recognizer(i)
    fishface.write(model_filename)
else:

    for i in range(0,10):
        correct = run_recognizer()
        print ("got {} percent correct!" .format(correct))
    metascore.append(correct)

print ("\n\nend score: {} percent correct!".format(np.mean(metascore)))
