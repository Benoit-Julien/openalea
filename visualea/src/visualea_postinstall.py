""" Postinstall scripts"""

__license__ = "Cecill-C"
__revision__ = " $Id: visualea_postinstall.py 1586 2009-01-30 15:56:25Z cokelaer $"


def install():
    
    from openalea.deploy.shortcut import create_win_shortcut, set_win_reg, create_fd_shortcut
    from openalea.deploy import get_base_dir
    import sys
    from os.path import join as pj

    # Get the location of the installed egg
    base_dir = get_base_dir('openalea.visualea')
    share_dir = pj(base_dir, 'share')
    
    winexe = sys.executable
    winexe = winexe.replace('python.exe', 'pythonw.exe')
        
    create_win_shortcut(name = 'Visualea',
                        target = winexe,
                        arguments = '"'+pj(sys.prefix, 'Scripts', 'visualea-script.pyw')+'"',
                        startin = "", 
                        icon = pj(share_dir, 'openalea_icon.ico'),
                        description = "Visual programming",
                        menugroup = "OpenAlea")

    create_win_shortcut(name = 'Python Shell',
                        target = winexe,
                        arguments = '"'+pj(sys.prefix, 'Scripts', 'aleashell-script.pyw')+'"',
                        startin = "", 
                        icon = "",
                        description = "Python Shell",
                        menugroup = "OpenAlea")
    
        

    #create_fd_shortcut(name='Visualea',
    #                   target=sys.executable, 
    #                   arguments=pj(sys.prefix, 'bin', 'visualea'), 
    #                   menugroup='OpenAlea', 
    #                   icon='' )
   


def uninstall():
    pass
