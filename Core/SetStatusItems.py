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
            if svn_settings().get('SVN.show_diff_in_status_bar', 0) == 1:
                controller.svnDir = controller.get_scoped_path('file')
                procText = controller.run_svn_command([ "svn", "status", controller.svnDir])

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