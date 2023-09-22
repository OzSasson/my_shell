import glob
import os, shutil, datetime

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
        print(1)


def main():
    while True:
        cmd = input(f'{os.getcwd()} :)')
        cmd = cmd.lower().strip()
        check_command(cmd)


if __name__ == '__main__':
    main()
