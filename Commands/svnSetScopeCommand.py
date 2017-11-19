import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime

from ..Core.Controller import *

def svn_settings():
    return sublime.load_settings( 'Preferences.sublime-settings' )

selfSettings = svn_settings()

class svnSetScopeCommand(sublime_plugin.ApplicationCommand, svnController):

    def run(self, scope):
        global selfSettings
        selfSettings.set('SVN.commit_scope', scope)
        sublime.save_settings('Preferences.sublime-settings')

    def is_checked(self, scope):
        global selfSettings
        selScope = selfSettings.get('SVN.commit_scope', 5)
        print("-----------")
        print(selfSettings.get('SVN.commit_scope', 'repo'))
        print(selfSettings)
        print(selScope)
        if selScope == None:
            selScope = 'dir'
        print(selScope)
        print(scope)
        print("-----------")
        return selScope == scope
