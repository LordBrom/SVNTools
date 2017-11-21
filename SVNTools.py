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

from .Commands.svnCommitCommand import *
from .Commands.svnCommitLastCommand import *
from .Commands.svnCommitBlankCommand import *
from .Commands.svnCommitHistoryCommand import *


def plugin_loaded():
    sublime.avibeSVNToolsTicketNo = ""
    sublime.avibeSVNToolsThisComment = ""
    sublime.avibeSVNToolsLastComment = ""
    sublime.avibeSVNToolsScopes = ['Commit Scope: Full Repository','Commit Scope: Current File','Commit Scope: Current Directory']
    sublime.avibeSVNScopes = ['Current File','Current Directory','Full Repository']
    print("==============")
    print("loaded")
    print("==============")

class ChangeLog(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        procText = self.run_svn_command([ "svn", "log", "-v", self.svnDir]);

        show_output_panel(procText)

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
