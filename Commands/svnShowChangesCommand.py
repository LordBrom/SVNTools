import sublime
import sublime_plugin

from ..Core.Controller import *

class svnShowChangesCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path('file');

        procText = self.run_svn_command([ "svn", "diff", self.svnDir]);

        if len(procText):
            newView = sublime.active_window().new_file();
            newView.insert(edit, 0, procText);
            newView.set_syntax_file("Packages/Diff/Diff.tmLanguage");
            newView.set_scratch(True);
        else:
            sublime.status_message("The files match.");

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
