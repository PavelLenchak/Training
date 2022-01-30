from datetime import datetime, timedelta
from threading import Timer
import selenium
from selenium import webdriver
import time
import sys, os

# Библиотеки для записи видео
import subprocess as subp
from os.path import join
import pyautogui


log_dir = 'C:\\Users\\LENOVO-PC\\Desktop\\Test video recording' # путь куда положить файл с записью
CORE_DIR = 'C:\\Users\\LENOVO-PC\\Desktop\\Test video recording' # путь где лежит ffmpeg.exe
video_file = join(log_dir, 'video_' + 'TEST' + '.avi')
FFMPEG_BIN = join(CORE_DIR, 'ffmpeg\\bin\\ffmpeg.exe')

AZH = "http://b21523.vr.mirapolis.ru/mira/miravr/1967969258"
# TOSUM = "http://b21523.vr.mirapolis.ru/mira/miravr/1716327600"

START = [15, 39, 0]
STOP  = timedelta(hours=1, minutes=35, seconds=0)

now = datetime.today()
print(f'Start program at {now.strftime("%Y-%m-%d - %H:%M:%S")}')
start_recording = now.replace(day=now.day, 
                            hour=START[0], 
                            minute=START[1],
                            second=START[2], 
                            microsecond=0)
if start_recording < now:
    print('Ошибка ввода - введите корректное время')
    sys.exit()
start_delta_t = start_recording - now
start_secs = start_delta_t.seconds + 1

stop_recording = start_recording + STOP

print(f'START RECORDING - {start_recording.strftime("%Y-%m-%d - %H:%M:%S")}')
print(f'STOP RECORDING - {stop_recording.strftime("%Y-%m-%d - %H:%M:%S")}')


def test():
    driver = webdriver.Chrome()
    driver.get('https://www.google.ru/')

    # command = [
    #     FFMPEG_BIN,
    #     '-y', # Overwrite output files without asking (if find the same name)
    #     '-loglevel', 'error', # Show all errors, including ones which can be recovered from
    #     '-f', 'gdigrab',
    #     '-framerate', '12',
    #     '-i', 'desktop',
    #     '-s', '960x540',
    #     '-pix_fmt', 'yuv420p',
    #     '-c:v', 'libx264',
    #     '-profile:v', 'main',
    #     '-fs', '50M', # Set the file size limit (bytes)
    #     video_file
    # ]
    # command = [
    #     FFMPEG_BIN,
    #     '-y',
    #     '-loglevel', 'debug',
    #     '-f', 'gdigrab',
    #     '-i', 'desktop',
    #     '-s', '960x540',
    #     '-framerate', '12',
    #     '-probesize', '10M',
    #     '-rtbufsize', '100M',
    #     '-c:v', 'libx264',
    #     '-r', '30',
    #     '-preset', 'ultrafast',
    #     '-tune', 'zerolatency',
    #     '-crf', '25',
    #     '-pix_fmt', 'yuv420p',
    #     '-profile:v', 'main',
    #     video_file
    # ]
    
    command = [
        FFMPEG_BIN,
        '-f', 'x11grab',
        '-s', '1024x768',
        '-r', '30',
        '-i', ':0',
        #'-f', 'alsa',
        #'-ac', '2',
        #'-ar', '48000',
        #'-i', 'hw:0',
        #'-vcodec', 'flashsv',
        #'-acodec', 'pcm_s16le',
        video_file
    ]

    ffmpeg = subp.Popen(command, stdin=subp.PIPE, stdout=subp.PIPE, stderr=subp.PIPE)

    print('We are waiting now')
    time.sleep(5)
    print('We waited 5 seconds')

    ffmpeg.stdin.write('q')
    ffmpeg.stdin.close()
    print("Programm is done")


def end_recording():
    pyautogui.press('F9')
    print(f'End recording at {datetime.today().strftime("%Y-%m-%d - %H:%M:%S")}')


def start_rec():
    print(f'Start recording at {datetime.today().strftime("%Y-%m-%d - %H:%M:%S")}')
    pyautogui.moveTo(390,2,duration=1)
    pyautogui.click()
    pyautogui.press('F9')

    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    driver.get(AZH)
    driver.fullscreen_window()
    time.sleep(5)

    name = driver.find_element_by_name('pfirstname').send_keys("Павел")
    last_name = driver.find_element_by_name('plastname').send_keys("Ленчак")
    group = driver.find_element_by_name('categoryid').send_keys("ХТм-201")

    botton = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[2]/div/form/div[2]/button').click()
    time.sleep(10)
    start_work_botton = driver.find_element_by_xpath('//*[@id="modal-root"]/div/div[2]/div/div[2]/button').click()

    # greetings = driver.find_element_by_tag_name('textarea').send_keys("Здравствуйте!")
    # bottons = driver.find_elements_by_tag_name('button')
    # bottons[1320].click()


    end_prog = Timer(STOP.seconds, end_recording)
    end_prog.start()


def main():
    start_prog = Timer(start_secs, start_rec)
    start_prog.start()


def off_pc():
    os.system('shutdown -s')

if __name__ == '__main__':
    main()
