import sublime
import sublime_plugin

from ..Core.Controller import *

class svnCommitLastCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        if( 0 == len( sublime.avibeSVNToolsLastComment )):
            sublime.status_message( "Commit with comment (CTRL-ALT-B twice) to use this shortcut." );
            return

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'file'))

        sublime.active_window().run_command("save")

        self.do_commit(sublime.avibeSVNToolsLastComment)

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
