import sublime
import sublime_plugin

from ..Core.Controller import *

class svnGetChangedFileListCommand(sublime_plugin.TextCommand, svnController):
    def run(self, edit):
        self.svnDir = self.get_svn_dir()
        if len(self.svnDir) == 0:
            return;

        self.svnDir = self.get_scoped_path('repo')

        self.fileList = list(svn_settings().get('SVN.history', []))
        # self.fileList.insert(min(len(self.fileList), 1), 'New Log')

        sublime.active_window().show_quick_panel(self.fileList, self.on_ticket)

    def on_ticket(self, index):
        try:
            message = self.fileList[index]

            if index == -1:
                pass
            else:
                print(message)
                # self.run_svn_command([], False, 'log', paths);
                procText = self.run_svn_command([ "svn", "log", "--search", message, "--verbose", self.svnDir]);
                self.get_file_list(procText, message)
                # print(procText)

        except ValueError:
            pass

    def is_enabled(self):
        return len(str(self.get_svn_dir())) != 0


    def get_file_list(self, logBlock, message):
        show_output_panel(logBlock)
        lineSplit = '------------------------------------------------------------------------'
        logList = logBlock.strip( ).split( lineSplit );
        print(logList)
        result = ''
        addedFileList = []
        modifiedFileList = []
        deletedFileList = []

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

            for file in fileList:
                if file[0] == 'M':
                    if not file in modifiedFileList:
                        modifiedFileList.append(file)
                elif file[0] == 'A':
                    addedFileList.append(file)

        result += 'Modified Files\n'
        result += '\n'.join([str(arrStr) for arrStr in modifiedFileList]) + '\n\n'
        result += 'Added Files\n'
        result += '\n'.join([str(arrStr) for arrStr in addedFileList]) + '\n'
        show_output_panel(result)
