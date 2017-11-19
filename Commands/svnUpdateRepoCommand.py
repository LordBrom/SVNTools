import sublime
import sublime_plugin

from ..Core.Controller import *

class svnUpdateRepoCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;
        self.edit = edit;
        sublime.status_message("Select update scope");
        self.confirmList = list(sublime.avibeSVNScopes)
        sublime.active_window().show_quick_panel(self.confirmList, self.do_Update)

    def do_Update(self, index):
        self.scope = ''
        if index == -1 :
            return
        elif index == 0:
            self.svnDir = self.get_scoped_path('file')
            self.scope = 'File'
        elif index == 1:
            self.svnDir = self.get_scoped_path('dir')
            self.scope = 'Directory'
        else:
            self.svnDir = self.get_scoped_path('repo')
            self.scope = 'Repository'

        procTextPre = self.run_svn_command([ "svn", "update", self.svnDir]);

        procText = procTextPre.strip( ).split( "\n" )[-1].strip( );

        if "At revision" in procText:
            procText = self.scope + " is already up to date."
        elif "Updated" in procText:
            view = sublime.active_window().active_view();
            sublime.set_timeout(functools.partial(view.run_command, 'revert'), 0)

            self.show_output_panel(procTextPre)
        else:
            procText = "Could not commit revision; check for conflicts or other issues."

        sublime.status_message(procText);

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
