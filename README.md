# CodeHawk

CodeHawk is a program built for coding competitions. From creating a problem folder to automating tests, CodeHawk automates away the tedious parts of coding competitions, allowing you to focus on what matters.

# Quick Start

## Starting on a New Problem

CodeHawk treats each problem as a directory. Since contest problems are (usually) disjoint, using separate folders helps declutter your working directory. Thus, the first thing that CodeHawk does is to create a directory.

    > hawk problem_A
    Creating problem_A... Done!
    hawk>

Here, CodeHawk creates directory ```problem_A``` and enters an interactive shell in that directory. We can run normal shell commands such as ```pwd``` or ```echo```.

    hawk> echo 'Hellow, World!'
    Hello, World!
    hawk> pwd
    /Users/yuhanliu/Documents/CodingCompetitions/problem_A

## Creating Source Files

However, that's not too interesting. What CodeHawk also allows you to do is quickly create source files from predefined templates:

    hawk> start cpp
    Creating cpp source files... Done!
    hawk>

Note that the ```start``` command can likewise be invoked with just ```s```. You can even omit the programming language and CodeHawk will infer the language based on the last language used.

CodeHawk will create a file ```problem_A.<extension>```, where the file extension is the argument that ```start``` is passed. In the above example for example, CodeHawk will create the file ```problem_A.cpp```.

## Adding Testcases

Now, to add testcases we can use the ```add``` (or ```a```) command.

    hawk> add
    Adding testcase from clipboard... Done! Saved as testcase #1
    hawk>

By default, CodeHawk will extract the testcase from the contents of your clipboard. This is because testcases are usually given on a website, which can be easily copied onto the clipboard.

If the contents of your clipboard is empty, CodeHawk will get the testcase from ```stdin```.

    hawk> add
    3
    1 5 2
    Done! Saved as testcase #2
    hawk>

Just make sure to use ```Ctrl-D``` to terminate the testcase.

One can also explicitly use stdin by using the ```addstdin``` command.

    hawk> addstdin
    3
    1 5 2
    Done! Saved as testcase #3
    hawk>

Alternatively, we can add testcases by specifying them from a file.

    hawk> add /Users/yuhanliu/Downloads/testcase_1.in
    Adding testcase "/Users/yuhanliu/Downloads/testcase_1.in"... Done! Saved as testcase #4
    hawk>

CodeHawk will automatically place these testcases in the subdirectory ```.testcases/``` inside the problem directory, with each testcase labelled sequentially ```1.in```, ```2.in```, etc.

## Testing

Now, for the main part of the CodeHawk—testing! Testing is fairly simple with the ```test``` command.

    hawk> test
    Compiling... Done!
    Running on testcase #1
    ======================
    Input:
    3
    1 5 2
    ----------------------
    Output:
    1
    1 1 2 3 5
    1 1
    ======================
    
    Running on testcase #2
    ======================
    Input:
    3
    1 5 2
    ----------------------
    Output:
    1
    1 1 2 3 5
    1 1
    ======================
    ... (complete output truncated for README)
    hawk>

First, CodeHawk will compile (if necessary) the source files. Next, it will iterate through all the testcases and run the program on each one.

We can also test specific testcases by just passing the testcase number to the ```test``` command.

    hawk> test 2 4
    Source file not changed. No need for recompiling
    Running on testcase #2
    ======================
    Input:
    3
    1 5 2
    ----------------------
    Output:
    1
    1 1 2 3 5
    1 1
    ======================
    
    Running on testcase #4
    ======================
    Input:
    2
    3 2
    ----------------------
    Output:
    1 1 2
    1 1
    ======================
    hawk>

# Timeline
| Feature                       | Date |
| ----------------------------- | ---- |
| Basic CLI/Shell               | 3/20 |
| Configure Settings            | 3/27 |
| Adding Source Files/Testcases | 4/3  |
| Testing/Benchmarking          | 4/10 |