import subprocess
subprocess.call('clear', shell=True)

from pyzbar.pyzbar import decode
import cv2
import re
import time
try:
    cap = cv2.VideoCapture(0)
except NameError:
    exit()
users = [{'username': 'tobi', 'password': '1157', 'sudo': 'yes', 'authorized': 'no'}, {'username': 'gaelin', 'password': '1157', 'sudo': 'yes', 'authorized':'no'}]
current_user = ""
last_command = time.time()
last_command_text = ""

def get_formatted_text(result):
    return re.findall(r"data=b'(.*)', type", str(result))[0]


def get_dict_from_username(username):
    for item in users:
        if item['username'] == username:
            return item
    return False


def authorize_user(auth_string):
    global current_user
    auth_string_search = re.search(r"auth (.*):(.*)", auth_string)
    if auth_string_search:
        username = auth_string_search.group(1)
        password = auth_string_search.group(2)
        user = get_dict_from_username(username)
        if user:
            if user['password'] == password and not user['authorized'] == 'yes':
                user['authorized'] = 'yes'
                current_user = user['username']
                return True
            else:
                return False


def deauthorize_users():
    global current_user
    current_user = ""
    
def startv():
    deauthorize_users()
    subprocess.call('sudo ./runv.sh &', shell=True)

def stopv():
    subprocess.call('sudo pkill omxplayer', shell=True)    
    
def log(text):
    with open("log.txt", "a") as f:
        f.write("%s  %s %s\n" % (time.time(), current_user, text))

def long_log(text):
    with open("long_log.txt", "a") as f:
        f.write("%s  %s solve: %s\n" % (time.time(), current_user, text))

def out(title, message):
    subprocess.call("notify-send -u 'critical' '{}' '{}' ".format(title, message), shell=True)
    print("Message: {} , {} sent!".format(title, message))

def main():
    global last_command
    global last_command_text
    global current_user
    _,cv2_im = cap.read()
    cv2_im = cv2.cvtColor(cv2_im, cv2.COLOR_BGR2RGB)
    solve = decode(cv2_im)
    if solve:
        long_log(solve)
    for qr_code in solve:
        command = get_formatted_text(qr_code)
        if time.time() < (last_command + 2.0):
            return
        last_command = time.time()
        log(command)
        
        ##User is not logged in
        if 'startv' == command:
            startv()
            out("Info", "Started")
            return
            
        elif 'auth' in command:
            if authorize_user(command):
                stopv()
                out("Authorized Successfully", "Welcome {}".format(current_user))
                return
        
        if current_user is "":
            out("Error!", "Not authorized")
            return

        ##User is logged in
        if 'deauth' == command:
            out("Deauthorized", "Goodbye {}".format(current_user))
            deauthorize_users()
            startv()
            
        elif 'stopv' == command:
            stopv()
            out("Info", "Stopped")
            
        elif 'exit' == command:
            out("Exiting", "Goodbye")
            exit()
            
        elif 'run' in command:
            plain_command = re.findall(r"run (.*)", command)[0]
            out("Ran command", plain_command)
            subprocess.call('%s &' % plain_command, shell=True)
            last_command_text = plain_command
            
        elif 'shutdown' == command:
            subprocess.call('poweroff', shell=True)


if __name__ == '__main__':
    log("Started")
    subprocess.call("/usr/lib/notification-daemon/notification-daemon &", shell=True)
    startv()
    while True:
        main()