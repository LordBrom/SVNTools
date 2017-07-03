import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime
import threading

def svn_settings():
    return sublime.load_settings( 'Preferences.sublime-settings' )