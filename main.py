import os, shutil, datetime
import glob
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

path=[]
path_s=r'C:\3.11\Scripts\;C:\3.11\;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem;C:\WINDOWS\System32\WindowsPowerShell\v1.0\;C:\WINDOWS\System32\OpenSSH\;C:\Program Files\dotnet\;C:\Program Files\Microsoft SQL Server\130\Tools\Binn\;C:\Program Files\Microsoft SQL Server\Client SDK\ODBC\170\Tools\Binn\;C:\310\Scripts\;C:\310\;C:\Users\shaha\AppData\Local\Microsoft\WindowsApps;C:\Users\shaha\.dotnet\tools;;C:\Program Files\JetBrains\PyCharm Community Edition 2022.2\bin;'
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


def make_path():
    global path
    global path_s
    ls=path_s.split(';')
    for i in range(0,4):
        path.append(ls[i])
    print(path)
def exiT():
    pass


def seT():
    pass


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


def run_exe(lst1):
    global path
    if lst1[0].endswith('.py'):
        lst1 = ['python.exe'] + lst1
    if lst1[0].endswith('.exe'):
        s = os.path.join(os.getcwd(), lst1[0])
        if os.path.exists(s):
            lst1[0] = s
            result = subprocess.run(lst1, stdin=None, stdout=None, stderr=None, shell=True)
        else:
            for i in path:
                s = os.path.join(i, lst1[0])
                if os.path.exists(s):
                    lst1[0] = s
                    result = subprocess.run(lst1, stdin=None, stdout=None, stderr=None, shell=True)
                    break
            else:
                print(
                    f"Error: The executable '{lst1[0]}' was not found in the current directory or in the specified path.")
    else:
        print(
            f"Error: The executable '{lst1[0]}' was not found in the current directory or in the specified path.")


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


def check_command(inp):
    ls = inp.split(" ")
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
    elif ls[0] == 'set':
        return seT()
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
        seT()
    else:
        run_exe(ls)


def main():
    make_path()
    while True:
        cmd = input(f'{os.getcwd()} :)')
        cmd = cmd.lower().strip()
        check_command(cmd)


main()