import requests
import soundfile

def download_speech(url):
    url=url
    r = requests.get(url,stream=True,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    print(r.encoding) #None is good (bytes-->audio),iso is bad (text),User-Agent very important
    with open('my_test_capcha.wav', 'wb+') as f:
            if r.status_code == requests.codes.ok:
                f.write(r.content)
                print('yes')
            else:
                print(r.status_code,requests.codes.ok)
                print('no')

    f.close()
    data, samplerate = soundfile.read('my_test_capcha.wav')
    soundfile.write('new.wav', data, samplerate, subtype='PCM_16')
