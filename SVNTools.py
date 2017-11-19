import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime

from .Core.Controller import *

from .Commands.svnSetScopeCommand import *
from .Commands.svnAddFileCommand import *
from .Commands.svnRepoStatusCommand import *
from .Commands.svnUpdateRepoCommand import *
from .Commands.svnDiscardChangesCommand import *
from .Commands.svnShowChangesCommand import *


def plugin_loaded():
    sublime.avibeSVNToolsTicketNo = ""
    sublime.avibeSVNToolsThisComment = ""
    sublime.avibeSVNToolsLastComment = ""
    sublime.avibeSVNToolsScopes = ['Commit Scope: Full Repository','Commit Scope: Current File','Commit Scope: Current Directory']
    sublime.avibeSVNScopes = ['Current File','Current Directory','Full Repository']
    print("==============")
    print("loaded")
    print("==============")

def svn_settings():
    return sublime.load_settings( 'Preferences.sublime-settings' )

def svn_set_status_items(self, view):

    if svn_settings().get('SVN.show_status_bar_info', 1) == 1:
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            view.set_status('AAAsvnTool', 'SVN:' + u'\u2718')
            view.erase_status('AABsvnTool')
            view.erase_status('AACsvnTool')
        else:
            view.set_status('AAAsvnTool', 'SVN:' + u'\u2714')
            view.set_status('AABsvnTool', 'Scope: ' + str(svn_settings().get('SVN.commit_scope', 'repo')))
            if svn_settings().get('SVN.show_diff_in_status_bar', 0) == 1:
                self.svnDir = self.get_scoped_path('file')
                procText = self.run_svn_command([ "svn", "status", self.svnDir])

                if len(procText):
                    procText = procText.split( '\n' )[0].strip( )
                    procText = procText.split( )[0]

                    if procText == 'M':
                        view.set_status('AACsvnTool', 'diff:' + u'\u2260' )
                    else:
                        view.set_status('AACsvnTool', 'diff:' + u'\u003D' )
                else:
                    view.set_status('AACsvnTool', 'diff:' + u'\u003D' )


            else:
                view.erase_status('AACsvnTool')
    else:
        view.erase_status('AAAsvnTool')
        view.erase_status('AABsvnTool')
        view.erase_status('AACsvnTool')





class ChangeLog(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        procText = self.run_svn_command([ "svn", "log", "-v", self.svnDir]);

        show_output_panel(procText)



class svnCommitCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'repo'))

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

class svnCommitLastCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        if( 0 == len( sublime.avibeSVNToolsLastComment )):
            sublime.status_message( "Commit with comment (CTRL-ALT-B twice) to use this shortcut." );
            return

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'repo'))

        sublime.active_window().run_command("save")

        self.do_commit(sublime.avibeSVNToolsLastComment)

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0

class svnCommitBlankCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'repo'))

        sublime.active_window().run_command("save")

        self.do_commit("")

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0

class svnCommitHistoryCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path(svn_settings().get('SVN.commit_scope', 'repo'))

        self.fileList = list(svn_settings().get('SVN.history', []))
        self.fileList.insert(min(len(self.fileList), 1), 'New Log')

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








class svnLogParser(svnController):
    def run(self):
        self.svnDir = self.get_scoped_path('repo')

        logLimit = svn_settings().get('SVN.log_limit', 1000)
        procText = self.run_svn_command([ "svn", "log", "-v", "--limit", str(logLimit), self.svnDir]);
        logList = procText.strip( ).split( '------------------------------------------------------------------------' );

        result = ''

        for log in logList:
            if len(log) == 0:
                continue

            splitLog = str(log + "|").strip().split( '\n' );
            # print(splitLog)

            logDetails = splitLog[0].split('|')
            revision   = logDetails[0].strip( )
            author     = logDetails[1].strip( )
            timeStamp  = logDetails[2].strip( )
            msgLines   = logDetails[3].strip( )
            msgCount = int(msgLines.split(" ")[0])

            splitLogLength = len(splitLog) - 1

            fileList = [splitLog[num].strip( ) for num in range(2, splitLogLength - (1 + msgCount))]

            messageArray = [splitLog[num].strip( ) for num in range(splitLogLength - msgCount, (splitLogLength - msgCount) + msgCount)]
            message = '\n'.join([str(arrStr).strip( ) for arrStr in messageArray])

            if len(message) == 0:
                message = 'No Commit Message'

            result += '------------------------------------------------------------------------------------------------------------------------------------------------\n'
            result += revision + ": " + author + ": " + timeStamp + '\n'
            result += message + '\n\n'
            result += 'File List:\n'
            result += '\n'.join([str(arrStr) for arrStr in fileList]) + '\n'
            result += '\n\n'



        self.show_output_panel(result)

class svnEventListener(sublime_plugin.EventListener, svnController):
    def on_activated_async(self, view):
        svn_set_status_items(self, view)

    def on_post_save_async(self, view):
        svn_set_status_items(self, view)
