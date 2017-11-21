import sublime
import sublime_plugin

from ..Core.Controller import *

class svnAddFileCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir();
        if len(self.svnDir) == 0:
            return;

        self.confirmList = ['Add current file to repo', 'Add current directory to repo']
        sublime.active_window().show_quick_panel(self.confirmList, self.do_Add)

    def do_Add(self, index):
        # print('added')
        self.scope = ''
        if index == -1 :
            return
        elif index == 0:
            self.svnDir = self.get_scoped_path('file')
            self.scope = 'File'
        else:
            self.svnDir = self.get_scoped_path('dir')
            self.scope = 'Directory'

        self.svnDir = self.get_scoped_path('file')
        procText = self.run_svn_command([ "svn", "add", self.svnDir]);
        procText = procText.strip( ).split( '\n' )[-1].strip( );

        if "Illegal target" in procText:
            procText = "Could not add file(s); check for conflicts or other issues."
        else:
            # print(procText)
            procText = "Added file(s) to repo"
        sublime.status_message(procText);

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
