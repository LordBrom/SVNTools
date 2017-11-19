import sublime
import sublime_plugin

from ..Core.Controller import *


class svnDiscardChangesCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;

        if sublime.ok_cancel_dialog("Are you sure you want to discard your changes?"):
            sublime.active_window().run_command("save")

            self.svnDir = self.get_scoped_path('file');

            sublime.status_message("file: " + str(self.svnDir));

            procText = self.run_svn_command([ "svn", "revert", self.svnDir]);
            procText = procText.strip( ).split( '\n' )[-1].strip( );

            if len(procText) == 0:
                procText = "There are no changes to discard."
            elif not "Reverted" in procText:
                procText = "Could not commit revision; check for conflicts or other issues."
            else:
                view = sublime.active_window().active_view();
                sublime.set_timeout(functools.partial(view.run_command, 'revert'), 0)

            sublime.status_message(procText);

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
