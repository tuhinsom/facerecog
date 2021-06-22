import glob
from shutil import copyfile

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotion order
participants = glob.glob("source_emotion/*") #Returns a list of all folders with participant numbers

for x in participants:
    part = "%s" %x[-4:] #store current participant number
    for sessions in glob.glob("%s/*" %x): #Store list of sessions for current participant
        #print(sessions+"\n")
        for files in glob.glob("%s/*" %sessions):
            
            current_session = files[20:-30]
            
            file = open(files, 'r')
            
            emotion = int(float(file.readline())) #emotions are encoded as a float, readline as float, then convert to integer.
            var_arr = glob.glob("source_images/{}/{}/*" .format(part, current_session))
            if len(var_arr) >0 :
                sourcefile_emotion = glob.glob("source_images/{}/{}/*" .format(part, current_session))[-1] #get path for last image in sequence, which contains the emotion
                
                sourcefile_neutral = glob.glob("source_images/{}/{}/*" .format(part, current_session))[0] #do same for neutral image
            
                dest_neut = "sorted_set/neutral/%s" %sourcefile_neutral[25:] #Generate path to put neutral image
                dest_emot = "sorted_set/%s/%s" %(emotions[emotion], sourcefile_emotion[25:]) #Do same for emotion containing image
            
                copyfile(sourcefile_neutral, dest_neut) #Copy file
                copyfile(sourcefile_emotion, dest_emot) #Copy file
            
