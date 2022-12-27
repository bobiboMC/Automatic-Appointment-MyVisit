import speech_recognition as sr
import soundfile
def speech_to_text(filename):
    filename=filename
    with sr.AudioFile(filename) as source:
        # initialize the recognizer
        r = sr.Recognizer()
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        #print(text)
        return text


if __name__=='__main__':
    data, samplerate = soundfile.read('my_test_capcha.wav')
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
    speech_to_text("new.wav")
