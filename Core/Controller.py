import sublime
import sublime_plugin
import os.path
import subprocess
import functools
import datetime

def svn_settings():
    return sublime.load_settings( 'Preferences.sublime-settings' )

def show_output_panel(outputStr):
    window = sublime.active_window()
    output = window.get_output_panel("SVN")

    output.run_command("insert", {"characters": outputStr})
    window.run_command("show_panel", {"panel": "output.SVN"})


class svnController():

    def get_svn_root_path(self):
        path = sublime.active_window().active_view().file_name( ).split( "\\" )

        svnFound = 0
        while 0 == svnFound and 0 != len( path ):
            path = path[:-1]
            currentDir = "\\".join( path )

            if os.path.isdir( currentDir + "\\.svn" ):
                return currentDir

        return ""

    def get_scoped_path(self, scope):
        filePath = sublime.active_window().active_view().file_name()
        repoPath = self.get_svn_root_path()

        if scope == 'repo':
            return repoPath
        elif scope == 'file':
            return filePath
        elif scope == 'dir':
            return os.path.dirname(filePath)
        else:
            return repoPath

    def get_svn_dir(self):
        try:
            self.svnDir = sublime.active_window().active_view().file_name( ).split( "\\" )

            svnFound = 0
            while 0 == svnFound and 0 != len( self.svnDir ):
                self.svnDir = self.svnDir[:-1]
                currentDir = "\\".join( self.svnDir )

                if os.path.isdir( currentDir + "\\.svn" ):
                    svnFound = 1

            if 0 == svnFound:
                return ""
        except:
            return ""

        return self.svnDir

    def run_svn_command(self, params, test = True, cmd = '', dir = ''):
        startupinfo = None
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        try:
            if test:
                proc = subprocess.Popen(
                            params,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            startupinfo=startupinfo)
            else:
                exePath = svn_settings().get('SVN.tortoiseproc_path', '')

                if not os.path.isfile(exePath):
                    sublime.error_message('can\'t find TortoiseProc.exe, please config setting file' '\n   --sublime-TortoiseSVN')

                proc = subprocess.Popen('"'+exePath+'"' + ' /command:' + cmd + ' /path:"%s"' % dir , stdout=subprocess.PIPE)

        except ValueError:
            print(ValueError)
            sublime.status_message( "SVN command failed." )
            return ""


        if test:
            return proc.communicate()[0].strip( ).decode()
        else:
            return 'done'

    def add_history(self, log):
        history = svn_settings().get('SVN.history', [])

        for item in list(history):
            if item == log:
                history.remove(item)

        history.reverse()
        history.append(log)
        history.reverse()
        svn_settings().set('SVN.history', history)
        sublime.save_settings('Preferences.sublime-settings')

    def do_commit(self, message):
        if self.svnDir == None:
            sublime.status_message( "No files selected to commit." )
            return

        if svn_settings().get('SVN.confirm_new_files_on_commit', 1):
            if self.first_commit(message):
                if sublime.ok_cancel_dialog("This file has not been commited to SVN using this message before. Would you like to continue?"):
                    test = 1
                else:
                    return

        procText = self.run_svn_command([ "svn", "commit", self.svnDir, "--message", message])

        procText = procText.strip( ).split( '\n' )[-1].strip( )

        if not "Committed revision" in procText:
            procText = "Could not commit revision; check for conflicts or other issues."

        self.add_history(message)

        sublime.status_message( procText + " (" + message + ")" )

    def first_commit(self, message):
        is_first_commit = 1

        activeFile = self.get_scoped_path('file')
        logLimit = svn_settings().get('SVN.log_limit', 1000)
        procText = self.run_svn_command([ "svn", "log", "--limit", str(logLimit), activeFile])
        lineArray = procText.strip( ).split( '\n' )

        for line in lineArray:
            if line[:1] == 'r':
                continue
            if line[:10] == '----------':
                continue
            if message in line:
                is_first_commit = 0
                break

        return is_first_commit
