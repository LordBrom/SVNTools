import sublime
import sublime_plugin

from ..Core.Controller import *


class svnShowLogCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit, paths=None):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;

        if paths == None:
            paths = self.get_scoped_path('file')
        else:
            paths = paths[0]

        self.run_svn_command([], False, 'log', paths);