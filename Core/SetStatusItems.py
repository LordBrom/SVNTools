import sublime
import sublime_plugin

from ..Core.Controller import *

def svn_set_status_items(self, view):
    controller = svnController()

    if svn_settings().get('SVN.show_status_bar_info', 1) == 1:
        controller.svnDir = controller.get_svn_dir()
        if len(controller.svnDir) == 0:
            view.set_status('AAAsvnTool', 'SVN:' + u'\u2718')
            view.erase_status('AABsvnTool')
            view.erase_status('AACsvnTool')
        else:
            view.set_status('AAAsvnTool', 'SVN:' + u'\u2714')
            view.set_status('AABsvnTool', 'Scope: ' + str(svn_settings().get('SVN.commit_scope', 'file')))

            if svn_settings().get('SVN.show_svn_status_in_status_bar', 1) == 1:
                controller.svnDir = controller.get_scoped_path('file')
                procText = controller.run_svn_command([ "svn", "status", '-u', controller.svnDir], stripResult = False)

                if len(procText):
                    procText = procText.split( '\n' )[0]
                    print('===================')
                    print("svn file status: '" + procText + "'")
                    print('===================')
                    responseCol1 = procText[0] #File modifications
                    responseCol2 = procText[1] #File/Dir properties
                    responseCol3 = procText[2] #Lock status
                    responseCol4 = procText[3] #Addition with history
                    responseCol5 = procText[4] #Switched
                    responseCol6 = procText[5] #Lock information
                    responseCol7 = procText[6] #Conflict
                    responseCol8 = procText[7] #Always Blank
                    responseCol9 = procText[8] #Updated on server
                    # http://svnbook.red-bean.com/en/1.8/svn.ref.svn.c.status.html
                    statusStr = ''
                    if   responseCol7 == 'C':
                        statusStr = statusStr + u'\u203C' + ' '

                    if   responseCol9 == '*':
                        statusStr = statusStr + u'\u23F3' + ' '

                    if   responseCol1 == 'M':
                        statusStr = statusStr + u'\u2260' + ' '
                    elif responseCol1 == 'A':
                        statusStr = statusStr + u'\u271A' + ' '
                    elif responseCol1 == 'D':
                        statusStr = statusStr + u'\u002D' + ' '
                    elif responseCol1 == '?':
                        statusStr = statusStr + u'\u2718' + ' '
                    else:
                        statusStr = statusStr + u'\u003D' + ' '
                    view.set_status('AACsvnTool', 'status:' + statusStr )

                else:
                    view.set_status('AACsvnTool', 'status:' + u'\u003D' )
            else:
                view.erase_status('AACsvnTool')
    else:
        view.erase_status('AAAsvnTool')
        view.erase_status('AABsvnTool')
        view.erase_status('AACsvnTool')
        view.erase_status('AADsvnTool')
