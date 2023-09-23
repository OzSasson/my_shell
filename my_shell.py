import datetime
import glob
import os
import shutil
import subprocess

func_dic = {
    'cd': 'Displays the name of or changes the current directory.',
    'copy': 'Copies one or more files from one location to another.',
    'del (or delete)': 'Deletes one or more files.',
    'dir': 'Lists the files and directories in the current directory.',
    'exit': 'Closes the Command Prompt window.',
    'move': 'Moves one or more files from one location to another.',
    'set': 'Sets environment variables.',
    'cls': 'Clears the screen.',
    'help': 'Shows what every command does'
}


def print_dict():
    global func_dic
    for key, value in func_dic.items():
        print(f' {key} : {value}')


def change_dir(dir):
    try:
        os.chdir(dir)
    except Exception:
        print(f"Directory '{dir}' not found.")


def helP(com):
    global func_dic
    if com in func_dic:
        print(f'It does this {com}: {func_dic[com]}')
    else:
        print(f'Command "{com}" not found in the dictionary.')


def exiT():
    exit()


def diR(path):
    try:
        entries = os.scandir(path)
        for entry in entries:
            info = entry.name
            if entry.is_dir():
                info = "[" + info + "]"
            file_size = entry.stat().st_size
            if file_size < 1024:
                file_size_str = str(file_size) + ' bytes'
            else:
                file_size_str = str(file_size / 1024) + ' KB'
            file_time = datetime.datetime.fromtimestamp(entry.stat().st_mtime).strftime('%Y-%m-%d %H:%M %p')
            print(f"{file_time} {file_size_str} {info}")
    except FileNotFoundError:
        print(f"Directory '{path}' not found.")
    except PermissionError:
        print(f"Permission denied to access directory '{path}'.")


def move(src_path, dst_path):
    try:
        if not os.path.exists(src_path):
            print(f"Error: {src_path} does not exist.")
            return

        shutil.move(src_path, dst_path)
    except Exception as e:
        print(f"Cant move")


def copy(src_path, dst_path):
    try:
        if not os.path.exists(src_path):
            print(f"Error: {src_path} does not exist.")
            return
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
    except Exception as e:
        print(f"Cant copy")


def cls():
    print("\033c", end="")


def deL(path):
    matching_paths = glob.glob(path)

    if not matching_paths:
        print(f'No files or folders match the pattern: {path}')
        return

    for path in matching_paths:
        try:
            if os.path.isfile(path):
                os.remove(path)
                print(f'Deleted file: {path}')
            elif os.path.isdir(path):
                shutil.rmtree(path)
                print(f'Deleted folder and its contents: {path}')
            else:
                print(f'Error: "{path}" is neither a file nor a directory.')
        except Exception as e:
            print(f'Error deleting {path}: {e}')


def seT(var=None):
    if var:
        if '=' not in var:
            var = var.upper()
            res = os.environ.get(var)
            if res:
                print(f'{var}={res}')
            else:
                print(f'Environment variable {var} not defined')
        else:
            var = var.split('=')
            os.environ[var[0]] = var[1]

    else:
        for var, value in os.environ.items():
            print(f"{var}={value}")


def run_exe(lst1, stdin=None, stdout=None, PIPE=False):
    global path
    if lst1[0].endswith('.py'):
        lst1 = ['python.exe'] + lst1
    if lst1[0].endswith('.exe'):
        s = os.path.join(os.getcwd(), lst1[0])
        if os.path.exists(s):
            lst1[0] = s
            if not PIPE:
                return subprocess.run(lst1, stdin=stdin, stdout=stdout, stderr=None, shell=True)
            else:
                return subprocess.Popen(lst1, stdin=stdin, stdout=stdout, stderr=None, shell=True)
        else:
            for i in path:
                s = os.path.join(i, lst1[0])
                if os.path.exists(s):
                    lst1[0] = s
                    if not PIPE:
                        return subprocess.run(lst1, stdin=stdin, stdout=stdout, stderr=None, shell=True)
                    else:
                        return subprocess.Popen(lst1, stdin=stdin, stdout=stdout, stderr=None, shell=True)
            else:
                print(
                    f"Error: The executable '{lst1[0]}' was not found in the current directory or in the specified path.")
    else:
        print(
            f"Error: The executable '{lst1[0]}' was not found in the current directory or in the specified path.")


path = []
path_s = r'C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\iCLS\;C:\Program Files\Intel\Intel(R) Management Engine Components\iCLS\;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files\Intel\Intel(R) Management Engine Components\DAL;C:\Program Files (x86)\Intel\Intel(R) Management Engine Components\IPT;C:\Program Files\Intel\Intel(R) Management Engine Components\IPT;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\NVIDIA Corporation\NVIDIA NvDLISR;C:\Users\Oz Sasson\AppData\Local\Microsoft\WindowsApps;D:\Microsoft VS Code\bin;C:\Program Files (x86)\NVIDIA Corporation\PhysX\Common;C:\Program Files\Microsoft SQL Server\130\Tools\Binn\;C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\;C:\Program Files\dotnet\;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\;%SYSTEMROOT%\System32\OpenSSH\;C:\Users\Oz Sasson\AppData\Local\Microsoft\WindowsApps;;D:\PyCharm Community Edition 2022.2\bin;;C:\Users\Oz Sasson\.dotnet\tools'


def make_path():
    global path
    global path_s
    ls = path_s.split(';')
    for i in range(0, len(ls)):
        path.append(ls[i])


def remove_clum(lst):
    new_lst = []
    for i in lst:
        if i != '':
            new_lst.append(i)
    return new_lst


def check_command(ls, stdin=None, stdout=None, PIPE=False):
    if ls[0] == 'cd':
        if len(ls) == 1:
            print(os.getcwd())
            return
        change_dir(ls[1])
    elif ls[0] == 'help':
        if len(ls) > 1:
            return helP(ls[1])
        else:
            print_dict()
    elif ls[0] == 'exit':
        return exiT()
    elif ls[0] == 'dir':
        if len(ls) > 1:
            return diR(ls[1])
        else:
            return diR(os.getcwd())
    elif ls[0] == 'move':
        if len(ls) != 3:
            print('Not enough parameters')
            return
        move(ls[1], ls[2])
    elif ls[0] == 'copy':
        if len(ls) != 3:
            print('Not enough parameters')
            return
        copy(ls[1], ls[2])
    elif ls[0] == 'cls':
        cls()
    elif ls[0] == 'del':
        if len(ls) != 2:
            print('Not enough parameters')
            return
        deL(ls[1])
    elif ls[0] == 'set':
        if len(ls) == 2:
            seT(ls[1])
            return
        seT()
    else:
        return run_exe(ls, stdin, stdout,PIPE)


def check_pipe_or_redirect(ls):
    if '|' in ls[1:len(ls) - 1]:
        pipe(ls)
        return True
    elif '>' in ls[1:len(ls) - 1]:
        redirect_right(ls)
        return True
    elif '<' in ls[1:len(ls) - 1]:
        redirect_left(ls)
        return True
    return False


def redirect_right(ls):
    lst1, s = split_lst(ls, '>')
    with open(s, 'w') as f:
        check_command(lst1, None, f)


def redirect_left(ls):
    lst1, s = split_lst(ls, '<')
    if os.path.exists(s):
        with open(s, 'r') as f:
            check_command(lst1, f, None)
    else:
        print(f'Cant find {s}')


def split_pipe(ls):
    s = " ".join(ls)
    a = s.split('|')
    t = []
    for i in a:
        lst1 = i.split(' ')
        lst1 = remove_clum(lst1)
        t.append(lst1)
    return t


def pipe(ls):
    ls = split_pipe(ls)
    r = check_command(ls[0], None, subprocess.PIPE, True)
    ls = ls[1:]
    for i in range(len(ls) - 1):
        r1 = check_command(ls[i], r.stdout, subprocess.PIPE, True)
        r.stdout.close()
        r = r1
    r = check_command(ls[len(ls) - 1], r.stdout, None, True)
    print(r.communicate())


def split_lst(ls, st):
    new_lst = []
    s = ''
    for i in range(len(ls)):
        if ls[i] == st:
            if i < len(ls) - 1:
                s = ls[i + 1]
            break
        new_lst.append(ls[i])
    return new_lst, s


def main():
    make_path()
    while True:
        cmd = input(f'{os.getcwd()} :)')
        cmd = cmd.lower().strip().split(" ")
        cmd = remove_clum(cmd)
        if not check_pipe_or_redirect(cmd):
            check_command(cmd)


if __name__ == '__main__':
    main()
