import sublime
import sublime_plugin

from ..Core.Controller import *

sublime.SVNToolsLastMessage = []

class svnCommitCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'file'))

        sublime.active_window().run_command("save")

        self.new_message()
        pass

    def new_message(self):
        self.message_placeholders = svn_settings().get('SVN.message_placeholders', ['message'])
        self.placeholders_filled = [];
        self.index = 0;

        self.message_prompt();

    def message_prompt( self ):
        prompt = self.message_placeholders[self.index];
        lastMessage = ""
        if len(sublime.SVNToolsLastMessage) > self.index:
            lastMessage = sublime.SVNToolsLastMessage[self.index]
        sublime.active_window().show_input_panel(prompt + ":", lastMessage, self.on_submit, None, None)

    def on_submit(self, text):
        try:
            self.placeholders_filled.append(text)
            self.index += 1
            if self.index < len(self.message_placeholders):
                self.message_prompt()
            else:
                finalMessage = svn_settings().get('SVN.message_template', '[0]')

                sublime.SVNToolsLastMessage = self.placeholders_filled

                for index in range(len(self.message_placeholders)):
                    finalMessage = finalMessage.replace("["+ str(index) +"]", self.placeholders_filled[index])
                self.on_comment(finalMessage)
        except ValueError:
            pass

    def on_comment(self, text):
        self.do_commit(text)

    def is_enabled(self):
        return True
        return len(str(self.get_svn_dir())) != 0
