import subprocess

class Runner(object):
    def __init__(self) -> None:
        pass

    def run_command(self,cmd_and_args, print_constantly=False, cwd=None):
        """
        Runs a system command.

        args:
            cmd_and_args: the command to run with or without a Pipe (|).
            print_constantly: If True then the output is logged in continuous until the command ended.
            cwd: the current working directory (the directory from which you will like to execute the command)
        
        return: 
            - a tuple containing the return code, the stdout and the stderr of the command
        
        """
        output = []

        process = subprocess.Popen(cmd_and_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

        while True:
            next_line = process.stdout.readline()
            if next_line:
                output.append(str(next_line))
                if print_constantly:
                    print(next_line)
            elif not process.poll():
                break

        error = process.communicate()[1]

        return process.returncode, output, error

commander = Runner()