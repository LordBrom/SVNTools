import sublime
import sublime_plugin

from ..Core.Controller import *


class svnShowLogCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;

        self.run_svn_command([ "svn", "log", self.svnDir]);