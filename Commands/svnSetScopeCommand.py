import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime

from ..Core.Controller import *

class svnSetScopeCommand(sublime_plugin.ApplicationCommand, svnController):

    def run(self, scope):
        svn_settings().set('SVN.commit_scope', scope)
        sublime.save_settings('Preferences.sublime-settings')
        sublime.status_message( "Commit scope set to " + scope );

    def is_checked(self, scope):
        selScope = svn_settings().get('SVN.commit_scope', 'file')
        return selScope == scope
