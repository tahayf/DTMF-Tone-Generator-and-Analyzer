import numpy as np
import matplotlib.pyplot as plt 
from scipy.io import wavfile
from scipy import signal

def makeSine(amplitude,duration,freq,lowF,highF):
    time = np.linspace(0,duration,int(freq*duration))
    sine1 = amplitude*np.sin(2*np.pi*highF*time)
    sine2 = amplitude*np.sin(2*np.pi*lowF*time)
    return sine1+sine2

duration = 0.1
amplitude = 0.5
freq = 8000
silence = 0*np.linspace(0,duration,int(freq*duration))

hifreq = [1209,1336,1477]
lofreq = [697,770,852,941]
freqs = [697,770,852,941,1209,1336,1477] # need for comparing

keys = []
voice = []
voiceParts = []
voiceNum = []
ornekParts = []
ornekNum = []

for i in lofreq:
    for j in hifreq:
        sine = makeSine(amplitude,duration,freq,i,j)
        keys.append(sine)

number = list(input("Enter your number(without spaces): "))

for i in number:
    if (i == '0'):
        voice = np.append(voice,keys[10])
        voice = np.append(voice,silence)
    else:
        voice = np.append(voice,keys[int(i)-1])
        voice = np.append(voice,silence)


wavfile.write("aptal.wav",freq,voice)
fO,ornek = wavfile.read("Ornek.wav")
esikDeger = 1 # 0-1 
order = 2 # order of the filter

b, a = signal.butter(order,esikDeger/(fO/2),"high") # 'b' is numerator coefficent vector of the filter 'a' is denominator coefficent vector of the filter 
ornek = signal.filtfilt(b,a,ornek) # we filtered 0 frequency waves because 0 has DC value which is peak

# Our voice has 0.1 duration for each silence and number 
# Which is equal to 11 numbers and 11 silence 11+11 = 22 parts 
# Let's split the voice

counter = 0
voicediv22 = len(voice)/22
for i in range(22):
    voiceParts.append(voice[int(counter*voicediv22):int(counter*voicediv22+voicediv22)])
    counter += 1


for i in range(0,21,2):
    fftv = np.fft.fft(voiceParts[i])
    fftv_mag = np.abs(fftv[0:int(len(fftv)/2)])
    freqsfft = np.fft.fftfreq(len(voiceParts[i]))
    max = np.argmax(np.abs(fftv_mag))
    Hz1 = abs(freqsfft[max]*freq)
    fftv_mag[max] = 0 # We need to find the second max number
    max = np.argmax(np.abs(fftv_mag))
    Hz2 = abs(freqsfft[max]*freq)

    for j in freqs: # trying to find approximate frequencies tolerance is 5
        if (Hz1-5<j) and (Hz1+5>j):
            Hz1 = j
        if (Hz2-5<j) and (Hz2+5>j):
            Hz2 = j

        if (Hz1<Hz2):
            HzLow = Hz1
            HzHigh = Hz2
        else:
            HzLow = Hz2
            HzHigh = Hz1
    
    if (HzLow == lofreq[0] and HzHigh == hifreq[0]):
        voiceNum.append(1)
    elif (HzLow == lofreq[0] and HzHigh == hifreq[1]):
        voiceNum.append(2)
    elif (HzLow == lofreq[0] and HzHigh == hifreq[2]):
        voiceNum.append(3)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[0]):
        voiceNum.append(4)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[1]):
        voiceNum.append(5)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[2]):
        voiceNum.append(6)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[0]):
        voiceNum.append(7)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[1]):
        voiceNum.append(8)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[2]):
        voiceNum.append(9)
    elif (HzLow == lofreq[3] and HzHigh == hifreq[1]):
        voiceNum.append(0)
print(voiceNum)

# Question 3
counter = 0
ornekdiv22 = len(ornek)/22
for i in range(22):
    ornekParts.append(ornek[int(counter*voicediv22):int(counter*voicediv22+voicediv22)])
    counter += 1


for i in range(0,21,2):
    ffto = np.fft.fft(ornekParts[i])
    ffto[0] = 0
    ffto_mag = np.abs(ffto[0:int(len(ffto)/2)])
    freqsfft = np.fft.fftfreq(len(ornekParts[i]))
    max = np.argmax(np.abs(ffto_mag))
    Hz1 = abs(freqsfft[max]*fO)
    ffto_mag[max] = 0 # We need to find the second max number
    max = np.argmax(np.abs(ffto_mag))
    Hz2 = abs(freqsfft[max]*fO)

    for j in freqs: # trying to find approximate frequencies tolerance is 5
        if (Hz1-5<j) and (Hz1+5>j):
            Hz1 = j
        if (Hz2-5<j) and (Hz2+5>j):
            Hz2 = j

        if (Hz1<Hz2):
            HzLow = Hz1
            HzHigh = Hz2
        else:
            HzLow = Hz2
            HzHigh = Hz1
    
    if (HzLow == lofreq[0] and HzHigh == hifreq[0]):
        ornekNum.append(1)
    elif (HzLow == lofreq[0] and HzHigh == hifreq[1]):
        ornekNum.append(2)
    elif (HzLow == lofreq[0] and HzHigh == hifreq[2]):
        ornekNum.append(3)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[0]):
        ornekNum.append(4)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[1]):
        ornekNum.append(5)
    elif (HzLow == lofreq[1] and HzHigh == hifreq[2]):
        ornekNum.append(6)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[0]):
        ornekNum.append(7)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[1]):
        ornekNum.append(8)
    elif (HzLow == lofreq[2] and HzHigh == hifreq[2]):
        ornekNum.append(9)
    elif (HzLow == lofreq[3] and HzHigh == hifreq[1]):
        ornekNum.append(0)
print(ornekNum)



