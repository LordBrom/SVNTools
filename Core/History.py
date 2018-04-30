import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime

from ..Core.Controller import *


def svn_history():
	return sublime.load_settings( 'SvnMessageHistory.sublime-settings' )

class svnHistory():
	def get_history(includeNewLogOption = False, newLogText = 'New Log', getLast = False):
		messageHistory = list(svn_history().get('history', []))
		if includeNewLogOption:
			messageHistory.insert(min(len(messageHistory), 1), newLogText)
		if getLast:
			if len(messageHistory) == 0:
				messageHistory = ''
			else:
				messageHistory = messageHistory[0]
		return messageHistory

	def add_history(log):
		history = svn_history().get('history', [])

		for item in list(history):
			if item == log:
				history.remove(item)

		history.reverse()
		history.append(log)
		history.reverse()
		svn_history().set('history', history)
		sublime.save_settings('SvnMessageHistory.sublime-settings')