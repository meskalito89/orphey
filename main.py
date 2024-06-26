from PitchLession import PitchLession
import re
import pydub
import tempfile
import random
import os

from pdb import set_trace
REPEAT = 2
SOUND_FONT = 'sound_fonts/Yamaha_C3_Grand_Piano.sf2'
MIN_NOTE = 60
MAX_NOTE = 80
MAX_DISTANCE = 12
COUNT_OF_LESSIONS = 20
LESSION_PATH = 'lession'

ANSWERS = [
    'answers/0.wav',
    'answers/1.wav',
    'answers/2.wav',
    'answers/3.wav',
    'answers/4.wav',
    'answers/5.wav',
    'answers/6.wav',
    'answers/7.wav',
    'answers/8.wav',
    'answers/9.wav',
    'answers/10.wav',
    'answers/11.wav',
    'answers/12.wav',
]

def clear_lession_folder():
    for file in os.scandir(LESSION_PATH):
        os.remove(file)

def main():
    files = []
    for i in range(COUNT_OF_LESSIONS):
        random_note = random.randint(60, 80)
        distance1 = random.randint(0, 12)
        distance_is_greather_then_0 = random.choice([-1, 1])
        distance2 = distance1 * distance_is_greather_then_0
        l = PitchLession(sound_font='sound_fonts/Yamaha_C3_Grand_Piano.sf2', note=random_note, distance=distance2, repeat=2)
        pitch_file = l.to_temporary_file()
        pitch = pydub.AudioSegment.from_wav(pitch_file.name)
        files.append(pitch)
        answer = pydub.AudioSegment.from_wav(ANSWERS[distance1])
        files.append(answer)
    
    combined = files[0]
    for wav in files[1:]:
        combined = combined.append(wav)

    with open('meta.txt', 'r+') as file:
        key, last_file_name = file.readline().split("=")
        key = key.strip()
        last_file_name = last_file_name.strip()
        file.seek(0)
        clear_lession_folder()
        file_name, number = last_file_name.split('_')
        file_name = file_name.strip()
        new_number = int(number) + 1
        new_file_name = '_'.join([file_name, str(new_number)])
        file.write(f'{key}={new_file_name}')
        new_path = os.path.join(LESSION_PATH, new_file_name+'.mp3')
        with open(new_path, 'wb') as result:
            combined.export(result.name, format='mp3')

if __name__ == "__main__":
    main()
