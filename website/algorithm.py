import numpy as np
import cv2

from sklearn import linear_model
from scipy import signal
from joblib import dump, load

reg = load('model.joblib') 

def convert(video_path):
    
    cap = cv2.VideoCapture(video_path)
    
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = 64
    frameHeight = 48
    print(frameCount,frameHeight,frameWidth)

    buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

    fc = 0
    ret = True

    while (fc < frameCount  and ret):
        read = cap.read()[1]
        if read is not None:

            read = cv2.resize(read, dsize=(64, 48), interpolation=cv2.INTER_NEAREST)
            read = cv2.cvtColor(read,cv2.COLOR_RGB2HSV)
            buf[fc] = read
            fc += 1
        else:
            buf[fc] = buf[fc-1]
            fc += 1

    diffs = np.abs(buf[1:]-buf[:-1])
    
    diffs = diffs.reshape(-1,frameWidth*frameHeight,3)

    diffs = np.median(diffs,axis=1)

    print(diffs.shape)
    
    h_peaks = signal.find_peaks(diffs[:,0],width=8)[0]
    s_peaks = signal.find_peaks(diffs[:,1],width=8)[0]
    v_peaks = signal.find_peaks(diffs[:,2],width=8)[0]
    
    print("found peaks")

    n_peaks = np.array([len(h_peaks),len(s_peaks),len(v_peaks)])
    
    median = np.median(diffs,axis=0)
    average = np.average(diffs,axis=0)

    print("computed averages")
    
    feature_set = np.concatenate((n_peaks,average,median),axis=0).reshape(1,-1)
    
    print("made feature set")

    print(reg.predict(feature_set)[0])

    return reg.predict(feature_set)[0]

def analyze(path):
    predicted_score = convert(path)

    cutoff = 0.22172396530318594

    if predicted_score > cutoff:
    	return True
    else:
    	return False

