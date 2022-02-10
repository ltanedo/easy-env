import glob
import os
import sys
import subprocess


def get_platform():
    '''
        input:  None
        output: (str) OS name 
    '''

    platform = sys.platform

    if platform == "linux" or platform == "linux2":
        return "LINUX"
    elif platform == "darwin":
        return "MAC"
    elif platform == "win32":
        return "WIN"
    else: 
        None


def get_shell():
    '''
        input:  None
        output: (str) shell name 
    '''

    if get_platform() == "MAC":
        return os.environ["SHELL"]
    
    return os.readlink('/proc/%d/exe' % os.getppid())


def get_rc_path():
    '''
        input:  None
        output: path of shell config file
    '''

    rc_path = "~/.bashrc"
    if "zsh" in get_shell():
        rc_path = "~/.zshrc"
    
    return rc_path


def set_unix_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''

    rc_path = get_rc_path()
    VAR_EXISTS = False
     
    # with is like your try .. finally block in this case
    with open(os.path.expanduser(rc_path), 'r') as file:
        data = file.readlines()
        for i, line in enumerate(data):
            pattern = f"export {key}="
            if pattern in line:
                data[i] =  f"export {key}='{value}';\n"
        
        if not VAR_EXISTS:
            data.append(f"export {key}='{value}';\n")

    # # and write everything back
    with open(os.path.expanduser(rc_path), 'w') as file:
        file.writelines( data )


def set_win_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''
    subprocess.run("SETX {0} {1} /M".format(key, value))



def set_universal_env_var(key, value):
    '''
        input:  (str) env_key , (str) env_value
        output: None
    '''

    platform = get_platform()

    if platform == "WIN":
        set_win_var(key,value)
    
    else:
       set_unix_var(key,value)
    