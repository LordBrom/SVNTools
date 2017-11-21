import sublime
import sublime_plugin

from ..Core.Controller import *

class svnCommitBlankCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'file'))

        sublime.active_window().run_command("save")

        self.do_commit("")

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
