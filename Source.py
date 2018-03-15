import in_defined_path_replacer as replace
import console_colors as console_color
import shutil
import os
main_path = ""
debug_mode = True


class ReadConfigFile:
    def __init__(self, file_name):
        self.config_file_name = file_name
        self.data_container = dict()

    def read_config_file(self):
        try:
            file_handler = open(self.config_file_name, 'r')
            main_path = file_handler.readline().strip('\'')
            for line in file_handler:
                if '#' in line:
                    continue
                tmp_list = line.split("\' \'")
                self.data_container[tmp_list[0].replace('\n', '').strip('\'').strip(' ')] = \
                    tmp_list[1].replace('\n', '').strip('\'').strip(' ')
        except IOError as e:
            print(console_color.Colors.WARNING +
                  "Config file reading error: {0} - {1}".format(e.errno, e.strerror) + console_color.Colors.ENDC)

    def get_tasks(self):
        return self.data_container


class RewriteRobots:
    def __init__(self, tmp):
        self.file_content = "User-agent: *\nDisallow: /images/\nDisallow: /private/"
        self.file_path = tmp
        self._rewrite()

    def _rewrite(self):
        fh = open(''.join([main_path, self.file_path]), 'w')
        fh.write(self.file_content)


class CopyDir:
    def __init__(self):
        try:
            shutil.copy2(''.join([main_path, '/html-beta']), ''.join([main_path, '/html']))
        except PermissionError as e:
            print(console_color.Colors.FAIL +
                  "Config file reading error: {0} - {1}".format(e.errno, e.strerror) + console_color.Colors.ENDC)


class TaskHandler:
    @staticmethod
    def replace_phrases(file_name):
        print(console_color.Colors.OKBLUE + 'Replace function test' + console_color.Colors.ENDC)
        if not debug_mode:
            replace.Controller(file_name)

    @staticmethod
    def rewrite_robots(file_path):
        print(console_color.Colors.OKBLUE + 'Rewrite function test' + console_color.Colors.ENDC)
        if not debug_mode:
            RewriteRobots(file_path)

    @staticmethod
    def cache_updater(file_path):
        print(console_color.Colors.OKBLUE + 'Cache update function test' + console_color.Colors.ENDC)
        if not debug_mode:
            os.system(file_path)


class TaskManager:
    def __init__(self):
        self.task_list = dict()
        self.task_handler = TaskHandler()

    def set_container(self, tmp_dict):
        self.task_list = tmp_dict

    def run_tasks(self):
        for element in self.task_list.keys():
            print("Key: {} with value: {}".format(element, self.task_list[element]))
            self.tasks_analyse(element, self.task_list[element])

    def tasks_analyse(self, key, val):
        if key == 'replace':
            self.task_handler.replace_phrases(val)
        elif str(key) == 'robots':
            self.task_handler.rewrite_robots(val)
        elif str(key) == 'cache':
            self.task_handler.cache_updater(val)
        else:
            print(console_color.Colors.FAIL + "There is not matching function!" + console_color.Colors.ENDC)


class DeployController:
    def __init__(self, config):
        self.config_file = config
        self.config_parser = ReadConfigFile(config)
        self.deploy_tasks = TaskManager()
        self.copy_files = CopyDir()
        self.run_deploy()

    def run_deploy(self):
        self.config_parser.read_config_file()
        self.deploy_tasks.set_container(self.config_parser.get_tasks())
        self.deploy_tasks.run_tasks()


def main(input_name):
    DeployController(input_name)


if __name__ == "__main__":
    import sys
    main((sys.argv[1]))