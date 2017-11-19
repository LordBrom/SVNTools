import sublime
import sublime_plugin

from ..Core.Controller import *


class svnRepoStatusCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_scoped_path('repo')
        procText = self.run_svn_command([ "svn", "status", self.svnDir]);
        self.show_output_panel(procText)

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
