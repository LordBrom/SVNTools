import sublime
import sublime_plugin

from ..Core.Controller import *

class svnCommitCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'file'))

        sublime.active_window().run_command("save")
        sublime.active_window().show_input_panel("Ticket number:", sublime.avibeSVNToolsTicketNo, self.on_ticket, None, None)
        pass

    def on_ticket(self, text):
        try:
            sublime.avibeSVNToolsTicketNo = text

            sublime.active_window().show_input_panel("Comment:", sublime.avibeSVNToolsThisComment, self.on_comment, None, None)
        except ValueError:
            pass

    def on_comment(self, text):
        sublime.avibeSVNToolsThisComment = text
        sublime.avibeSVNToolsLastComment = sublime.avibeSVNToolsTicketNo

        if len( sublime.avibeSVNToolsLastComment ):
            sublime.avibeSVNToolsLastComment = "#" + sublime.avibeSVNToolsLastComment + ": "

        sublime.avibeSVNToolsLastComment = sublime.avibeSVNToolsLastComment + sublime.avibeSVNToolsThisComment

        self.do_commit(sublime.avibeSVNToolsLastComment)

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0
