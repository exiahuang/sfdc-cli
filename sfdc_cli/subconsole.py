# special
import os, datetime
import threading
import subprocess
import platform
from .salesforce.myconsole import MyConsole
from . import logging

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"
IS_Linux = platform.system() == "Linux"


def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)


class SublConsole(MyConsole):

    def __init__(self):
        pass

    def info(self, obj):
        logging.info(obj)

    def error(self, obj):
        logging.error(obj)

    def debug(self, obj):
        logging.debug(obj)

    def log(self, msg):
        logging.info(msg)

    def showlog(self, obj, type='info', show_time=True):
        panel_name = "salesforcexytools-log-"
        if show_time:
            now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            now = now + "[" + type + "] "
            msg = now + str(obj)
        else:
            msg = str(obj)
        logging.info(msg)

    def show_in_dialog(self, message_str):
        logging.info(xstr(message_str))

    def status(self, msg, thread=False):
        if not thread:
            logging.debug(msg)
        else:
            self.status(msg)

    def handle_thread(self, thread, msg=None, counter=0, direction=1, width=8):
        if thread.is_alive():
            next = counter + direction
            if next > width:
                direction = -1
            elif next < 0:
                direction = 1
            bar = [' '] * (width + 1)
            bar[counter] = '='
            counter += direction
            self.status('%s [%s]' % (msg, ''.join(bar)))
            # sublime.set_timeout(
            #     lambda: self.handle_thread(thread, msg, counter, direction,
            #                                width), 100)
        else:
            self.status(' ok ')

    def save_and_open_in_panel(self,
                               message_str,
                               save_dir,
                               save_file_name,
                               is_open=True):
        save_path = os.path.join(save_dir, save_file_name)
        self.debug("save file : " + save_path)

        # delete old file
        if os.path.isfile(save_path):
            os.remove(save_path)

        # save file
        self.save_file(save_path, message_str)
        return save_path

    def save_file(self, full_path, content, encoding='utf-8'):
        if not os.path.exists(os.path.dirname(full_path)):
            self.debug("mkdir: " + os.path.dirname(full_path))
            os.makedirs(os.path.dirname(full_path))
        try:
            fp = open(full_path, "w", newline='\n', encoding=encoding)
            fp.write(content)
        except Exception as e:
            self.error('save file error! ' + full_path)
            self.error(e)
        finally:
            fp.close()

    def show_in_new_tab(self, message_str, name=None):
        view = self.window.new_file()
        view.settings().set('word_wrap', 'false')
        view.set_syntax_file('Packages/Java/Java.tmLanguage')
        if name:
            view.set_name(name)
        view.run_command("insert_snippet", {"contents": xstr(message_str)})

    def open_project(self, open_path):
        # executable_path = sublime.executable_path()
        executable_path = ""
        if IS_MAC:
            app_path = executable_path[:executable_path.rfind(".app/") + 5]
            executable_path = app_path + "Contents/SharedSupport/bin/subl"

        if IS_WINDOWS:
            subprocess.Popen('"{0}" --project "{1}"'.format(
                executable_path, open_path),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True)
        else:
            process = subprocess.Popen(
                [executable_path, '--project', open_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            self.debug(stdout)
            self.showlog(stderr)

    def open_in_new_tab(self, message, tab_name):
        view = self.window.new_file()
        view.run_command("new_view", {"name": tab_name, "input": message})

    def insert_str(self, message_str):
        self.window.run_command("insert_snippet",
                                {"contents": xstr(message_str)})

    def thread_run(self, group=None, target=None, name=None, args=()):
        thread = threading.Thread(target=target, args=args, name=name)
        thread.start()
        self.handle_thread(thread)
        return thread

    def close_views(self, main_path):
        for _view in self.window.views():
            file_name = _view.file_name()
            if file_name and main_path in file_name:
                _view.close()
