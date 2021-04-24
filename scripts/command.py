import os


class Command:

    def __init__(self, exec_path):
        self.curr_path = os.path.dirname(os.path.abspath(__file__))
        if isinstance(exec_path, list):
            self.exec_path = os.path.join(*exec_path)
        else:
            self.exec_path = exec_path

    def __call__(self, commands, chain=True):

        commands.insert(0, ['cd', self.curr_path])
        commands.insert(1, ['cd', self.exec_path])

        joined = ' && '.join([
            ' '.join(command).replace('%', self.curr_path)
                    for command in commands])

        print(joined)
        os.system(joined)
