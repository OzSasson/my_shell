import os

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
    pass


def seT():
    pass


def diR():
    pass

def check_command(inp):
    ls=inp.split(" ")
    if ls[0]=='cd':
        if len(ls) == 1:
            print(os.getcwd())
            return
        change_dir(ls[1])
    elif ls[0]=='help':
        if len(ls)>1:
            return helP(ls[1])
        else:
            print_dict()
    elif ls[0]=='exit':
        return exiT()
    elif ls[0]=='set':
        return seT()
    elif ls[0]=='dir':
        return diR()
    else:
        print(1)

def main():
    while True:
        cmd = input(f'{os.getcwd()} :)')
        cmd=cmd.lower().strip()
        check_command(cmd)

if _name_ == '__main__':
    main()
