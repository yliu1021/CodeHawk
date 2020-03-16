import os
import glob
import shutil

import pyperclip

import settings


def start(problem_name: str, argv: [str]):
    if len(argv) > 1:
        print('Too many arguments! Run "help start" for more information')
        return
    lang = argv[0] if len(argv) == 1 else settings.default_settings['lang']
    settings.default_settings['lang'] = lang
    file_name = problem_name + '.' + lang
    file_path = os.path.join(problem_name, file_name)

    def create_file():
        print(f'Creating file {file_name}')
        with open(file_path, 'w'):
            pass

    if not os.path.exists(file_path):
        create_file()
    else:
        overwrite = input(f'File {file_name} already exists. Overwrite? [y/N]: ')
        if overwrite.lower() == 'y':
            create_file()


def add(problem_name: str, argv: [str]):
    test_case_dir = os.path.join(problem_name, '.testcases')
    os.makedirs(test_case_dir, exist_ok=True)
    if len(argv) > 1:
        print('Too many arguments! Run "help add" for more information')

    testcases = glob.glob(os.path.join(test_case_dir, '[0-9]*.in'))
    if len(testcases) == 0:
        next_testcase_num = 1
    else:
        next_testcase_num = 1
        for testcase in testcases:
            last_testcase_name = testcase.split('/')[-1]
            next_testcase_num = max(next_testcase_num, int(last_testcase_name[:-3]) + 1)

    next_testcase_file = os.path.join(test_case_dir, f'{next_testcase_num}.in')

    def write_testcase(content):
        with open(next_testcase_file, 'w') as testcase_file:
            testcase_file.write(content)
        print(f'Done! Saved as test case #{next_testcase_num}')

    if len(argv) == 0:
        clipboard_contents = pyperclip.paste()
        if len(clipboard_contents) != 0 and not clipboard_contents.isspace():
            print('Reading test case from clipboard... ', end='')
            write_testcase(clipboard_contents)
            return
        else:
            print('Clipboard empty. Reading from stdin:')

    if len(argv) == 0 or argv[0] == 'stdin':
        stdin_contents = ''
        try:
            while True:
                stdin_input = input()
                stdin_contents += stdin_input + '\n'
        except EOFError:
            write_testcase(stdin_contents)
            return

    assert(len(argv) == 1)

    print('Copying test case...', end='')
    shutil.copy(argv[0], next_testcase_file)
    print(f'Done! Saved as test case #{next_testcase_num}')


def remove(problem_name: str, argv: [str]):
    if len(argv) != 1:
        print('Invalid arguments! Run "help remove" for more information')
        return

    test_case_dir = os.path.join(problem_name, '.testcases')
    test_case = os.path.join(test_case_dir, f'{argv[0]}.in')

    if os.path.exists(test_case):
        print(f'Removing test case #{test_case}')
        os.remove(test_case)
    else:
        print(f'Test case #{test_case} does not exist!')


def print_testcase(problem_name: str, argv: [str]):
    if len(argv) != 1:
        print('Invalid arguments! Run "help remove" for more information')
        return

    test_case_dir = os.path.join(problem_name, '.testcases')
    test_case = os.path.join(test_case_dir, f'{argv[0]}.in')

    if os.path.exists(test_case):
        with open(test_case, 'r') as test_case_file:
            print(test_case_file.read())
    else:
        print(f'Test case #{test_case} does not exist!')


def list_testcases(problem_name: str, argv: [str]):
    test_case_dir = os.path.join(problem_name, '.testcases')
    testcases = sorted(glob.glob(os.path.join(test_case_dir, '[0-9]*.in')), key=lambda x: int(x.split('/')[-1][:-3]))
    print(f'{len(testcases)} test cases:')
    print('\n'.join(testcases))


def compile(problem_name: str, argv: [str]):
    compiler = settings.default_settings['compiler']
    compiler_flags = ' '.join(settings.default_settings['compiler flags'])
    if compiler == '':
        print('No compiler detected!')
        return

    lang = settings.default_settings['lang']
    file_name = problem_name + '.' + lang

    os.system(f'cd {problem_name} && {compiler} {compiler_flags} {file_name}')


def test(problem_name: str, argv: [str]):
    test_case_dir = os.path.join(problem_name, '.testcases')
    testcases = sorted(glob.glob(os.path.join(test_case_dir, '[0-9]*.in')), key=lambda x: int(x.split('/')[-1][:-3]))
    if len(argv) > 0:
        # prune out test cases
        testcase_nums = set(map(lambda x: int(x), argv))
        for i in range(len(testcases) - 1, -1, -1):
            testcase_num = int(testcases[i].split('/')[-1][:-3])
            if testcase_num not in testcase_nums:
                del testcases[i]

    executable = settings.default_settings['executable']

    for testcase in testcases:
        testcase_num = int(testcase.split('/')[-1][:-3])
        header = f'Running test case #{testcase_num}'
        print(header)
        print('='*len(header))
        print('Input:')
        with open(testcase, 'r') as testcase_file:
            print(testcase_file.read())
        print('-'*len(header))
        print('Output:')
        testcase = '/'.join(testcase.split('/')[1:])
        os.system(f'cd {problem_name} && ./{executable} < {testcase}')
        print()
        print()


supported_commands = {
    'start': start,
    's': start,

    'add': add,
    'a': add,

    'remove': remove,
    'r': remove,

    'print': print_testcase,
    'p': print_testcase,

    'list': list_testcases,
    'l': list_testcases,

    'compile': compile,
    'c': compile,

    'test': test,
    't': test,
}


def run(problem_name):
    os.makedirs(problem_name, exist_ok=True)
    while True:
        raw_cmd = input(f'hawk:{problem_name}> ')
        raw_cmd = raw_cmd.split()
        cmd, argv = raw_cmd[0], raw_cmd[1:]

        if cmd == 'quit' or cmd == 'q':
            break
        elif cmd in supported_commands:
            supported_commands[cmd](problem_name, argv)
        else:
            print(f'Invalid command: {cmd}. Enter "help" for a list of supported commands')
