import sublime
import sublime_plugin

from ..Core.Controller import *
from ..Core.History import *

class svnCommitHistoryCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'file'))

        self.fileList = svnHistory.get_history(includeNewLogOption = True)

        sublime.active_window().show_quick_panel(self.fileList, self.on_ticket)

    def on_ticket(self, index):
        try:
            message = self.fileList[index]

            if index == -1:
                pass
            elif message == 'New Log':
                sublime.active_window().run_command('svn_commit')
            else:
                self.do_commit(message)

        except ValueError:
            pass

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
