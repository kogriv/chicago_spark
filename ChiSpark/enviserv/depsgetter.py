import sys
import os
import subprocess
import re

from .environcheck import EnvironCheck
from .envsfider import VenvsFinder
from .mylog import MyLogger
from .dictan import DictAnalyzer

class DepsGetter:
    def __init__(self):
        self.envilog = MyLogger(name='ech',create_level='INFO',enable_logging=True)
        self.da = DictAnalyzer(self.envilog, 30)
        self.venvsfinder = VenvsFinder(llev=30, envilog=self.envilog, verbose=False)
        self.ech = EnvironCheck(llev=30, envilog=self.envilog, verbose=False)
        self.envs_path_list_win = []
        self.envs_path_list_linux = []
        self.result_list = []
        self.grouped_paths = {
            'venv': {},
            'virtualenvs': {},
            'conda': {}
        }
        self.environments = {}
        self.errors = {}

    def get_venvs_paths(self, envs_path_list_win=None, envs_path_list_linux=None, verbose=False):
        """
        Searches for paths of virtual environments based on the operating system.

        Args:
        - envs_path_list_win (list, optional): List of paths to search for virtual environments on Windows. Defaults to None.
        - envs_path_list_linux (list, optional): List of paths to search for virtual environments on Linux. Defaults to None.
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - None
        """
        slash = '\\' if sys.platform == 'win32' else '/'
        home_path = os.environ['USERPROFILE'] if sys.platform == 'win32' else os.environ['HOME']

        if sys.platform == 'win32':
            if envs_path_list_win is None or envs_path_list_win == []:
                envs_path_list_win = [
                    #home_path + '\\.virtualenvs',
                    #home_path + '\\anaconda3\\envs',
                    #home_path + '\\Documents\\pro',
                    #home_path + '\\AppData\Local\Programs\Python',
                    'C:\\Projects'
                ]
            
            if verbose:
                print("Searching *activate names in difined paths...")

            for ptf in envs_path_list_win:
                if verbose:
                    print("Searching in:", ptf)
                res = self.venvsfinder.search_venvs_path(
                    path_find=ptf, shell='powershell', verbose=False)
                if res != [''] and res not in self.result_list:
                    self.result_list.extend(res)

                for path in self.result_list:
                    parts = path.split(slash)
                    if '.virtualenvs' in parts:
                        env_type = 'virtualenvs'
                        env_name = parts[parts.index('.virtualenvs') + 1]
                    elif 'anaconda3' in parts:
                        env_type = 'conda'
                        if len(parts)>parts.index('anaconda3') + 2:
                            env_name = parts[parts.index('anaconda3') + 2]
                        else: env_name = 'undef_short_path'
                    elif  'conda' in parts:
                        env_type = 'conda'
                        if len(parts)>parts.index('conda') + 2:
                            env_name = parts[parts.index('conda') + 2]
                        else: env_name = 'undef_short_path'
                    else:
                        env_type = 'venv'
                        env_name = parts[-3]
                    self.grouped_paths.setdefault(env_type, {}).update({env_name: path})
            if verbose:
                print("Attempting get windows base python paths")
                self.get_base_win_paths(verbose=verbose)

        if sys.platform.startswith('linux'):
            if envs_path_list_linux is None or envs_path_list_linux == []:
                if self.ech.container_id:
                    envs_path_list_linux = ["/"]
                else:
                    envs_path_list_linux = [
                        os.path.join(home_path, '.virtualenvs'),
                        os.path.join(home_path, 'anaconda3', 'envs'),
                        os.path.join(home_path, 'Documents', 'pro'),
                        '/Projects'
                    ]

            for ptf in envs_path_list_linux:
                res = self.venvsfinder.search_venvs_path(
                    path_find=ptf, shell='bash', verbose=True)
                if res != [''] and res not in self.result_list:
                    self.result_list.extend(res)

                for path in self.result_list:
                    parts = path.split('/')
                    if 'common' in parts:
                        if 'conda' in path:
                            self.grouped_paths['conda']['base'] = path
                        elif 'venv' in parts:
                            self.grouped_paths['venv']['base'] = path
                    elif 'bin' in parts and 'activate' in parts \
                        and 'conda' not in parts \
                        and '.virtualenvs' not in parts:
                        env_name = parts[-3]
                        self.grouped_paths['venv'][env_name] = path
                    elif 'bin' in parts and 'activate' in parts \
                        and 'conda' not in parts \
                        and '.virtualenvs' in parts:
                        env_name = parts[-3]
                        self.grouped_paths['virtualenv'][env_name] = path

    def get_conda_envs(self, verbose=False):
        """
        Retrieves a list of Conda environments.

        Args:
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - dict: A dictionary containing Conda environments where keys are environment names and values are paths.
        """
        conda_envs = {}

        try:
            conda_check = subprocess.run(
                ["conda", "--version"],
                capture_output=True,
                text=True
            )

            if conda_check.returncode != 0:
                if verbose:
                    print("Conda is not installed.")
                return {}
            else:
                if verbose:
                    print("Conda installed.")

            process = subprocess.Popen(
                ["conda", "env", "list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            conda_list = output.decode("utf-8")
            lines = conda_list.split('\n')[2:]
            #print(lines)

            for line in lines:
                if line:
                    venv_info = line.split()
                    if len(venv_info)>0:
                        venv_name = venv_info[0]
                        venv_path = venv_info[1] if len(venv_info) > 1 else ''
                        self.grouped_paths['conda'][venv_name] = venv_path
                        conda_envs[venv_name] = venv_path
                        #print(conda_envs)

        except Exception as e:
            if verbose:
                print("Error during processing conda execution output:", e)
        if verbose:
            print("Function get_conda_envs finished successfully")
        return conda_envs

    def get_dependencies_conda(self, conda_env_name, verbose=False):
        """
        Retrieves the dependencies of a Conda environment.

        Args:
        - conda_env_name (str): Name of the Conda environment.
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - dict: A dictionary containing the dependencies of the Conda environment where keys are package names and values are package versions.
        """
        packages = {}

        try:
            command = ["conda", "list", "-n", conda_env_name]
            if verbose:
                print("Attempting to run command:", command)

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            output, error = process.communicate()
            dependencies = output.decode("utf-8")

            if not '# packages in environment at' in dependencies:
                if verbose:
                    print("Invalid output of command: str (# packages in environment at) expected")
                return False
            if '\n' not in dependencies:
                if verbose:
                    print("Invalid output of command: there is no lines divider = \\n")
                return False

            lines = dependencies.split('\n')
            if len(lines) > 3 and not (len(lines) == 4 and lines[3] == ''):
                lines = lines[3:]
            else:
                if verbose:
                    print(f"There are no dependencies in this environment: {conda_env_name}")
                return {}

            for line in lines:
                if line and line != '':
                    package_info = line.split()
                    package_name = package_info[0]
                    package_version = package_info[1] if len(package_info) > 1 else None
                    packages[package_name] = package_version

            return packages
        except Exception as e:
            if verbose:
                print("Error during conda execution:", e)
            return False

    def check_venv_founded(self, package_manager, env_name, environments, verbose=False):
        """
        Checks if a virtual environment is found in the environments dictionary.

        Args:
        - package_manager (str): Name of the package manager (e.g., 'conda', 'venv').
        - env_name (str): Name of the virtual environment.
        - environments (dict): Dictionary containing information about virtual environments.
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - str or bool: Path of the virtual environment if found, False otherwise.
        """
        path = environments.get(package_manager, {}).get(env_name)
        if path is None:
            if verbose:
                print(f"Path for {package_manager}: {env_name} NOT found")
            return False
        elif path == '':
            if verbose:
                print(f"Path for {package_manager}: {env_name} is empty")
            return False
        return path

    def get_dependencies(self, package_manager, env_name, environments, verbose=False):
        """
        Retrieves dependencies for a specific virtual environment.

        Args:
        - package_manager (str): Name of the package manager (e.g., 'conda', 'venv').
        - env_name (str): Name of the virtual environment.
        - environments (dict): Dictionary containing information about virtual environments.
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - dict or False: A dictionary containing the dependencies of the virtual environment where keys are package names and values are package versions, or False if dependencies cannot be retrieved.
        """
        if verbose:
            print("Start getting dependencies...")

        dependencies = {}
        venv_path = self.check_venv_founded(package_manager, env_name, environments)
        shell_path = None

        if sys.platform.startswith('linux'):
            shell_path = os.environ.get('SHELL', '/bin/bash')
            command = f"source {venv_path} && pip list"
            if verbose:
                print('Linux shell path:', shell_path)

        if sys.platform == 'win32':
            shell_path = os.environ.get('COMSPEC', 'cmd.exe')
            if verbose:
                print('Windows shell path:', shell_path)
            command = f"{venv_path} && pip list"

        if verbose:
            print("venv_path = check_venv_founded():", venv_path)

        if venv_path:
            if package_manager == 'conda':
                dependencies = self.get_dependencies_conda(env_name, verbose)
                if verbose:
                    print("dependencies = get_dependencies_conda(env_name):", str(dependencies)[:50] + "....")
                return dependencies

            elif package_manager in ['virtualenvs', 'venv']:
                if 'base_python' not in env_name:
                    if verbose:
                        print(f'Attempting to use {package_manager} to run command:', command)

                    process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True,
                        executable=shell_path
                    )
                    output, error = process.communicate()

                    dependencies = {}
                    if output:
                        output_str = output.decode("utf-8")
                        lines = output_str.strip().split('\n')

                        if len(lines) == 3 and lines[2] == '':
                            if verbose:
                                print(f"There are no dependencies in this environment: {env_name}")
                            return {}

                        if len(lines) > 2:
                            lines = lines[2:]
                        else:
                            if verbose:
                                print("Invalid output: length of lines is less than 3")
                            return False

                        for line in lines:
                            parts = line.split()
                            package_name = parts[0]
                            package_version = parts[1] if len(parts) > 1 else None
                            dependencies[package_name] = package_version
                    return dependencies
                else:
                    if verbose:
                        print("'base_python' in env_name -> run get_base_win_deps()")
                    dependencies = self.get_base_win_deps(env_name,verbose=verbose)
                    print(dependencies)
                    return dependencies
        else:
            return False

    def get_all_dependencies(self, environments, verbose=True):
        """
        Retrieves dependencies for all virtual environments specified in the environments dictionary.

        Args:
        - environments (dict): Dictionary containing information about virtual environments.
        - verbose (bool, optional): Verbosity flag. Defaults to True.

        Returns:
        - None
        """
        if verbose:
            print("---------------------------------------------------------")
            print("- Function get_all_dependencies() started ---------------")
            print("- Getting all dependencies. This may take a while -------")

        for packman in ['virtualenvs', 'conda', 'venv']:
            if packman in environments:
                if verbose:
                    print("---------------------------------------------------------")
                    print(f"--packman = {packman} exists in venvs dict -------------")

                for env_name in environments[packman]:
                    if self.check_venv_founded(packman, env_name, environments):
                        if verbose:
                            print(f"Venv dict contains packman = {packman} | env_name = {env_name}")
                        dependencies = self.get_dependencies(packman, env_name, environments)
                        if dependencies:
                            if verbose:
                                print("---- Dependencies obtained! Dictionary will be added ----")
                        else:
                            if verbose:
                                print("---- Dependencies NOT obtained. Nothing will be added ----")
                            continue
                    else:
                        if verbose:
                            print(f"Venv dict does NOT contain packman = {packman} | env_name = {env_name}")
                        continue
            else:
                if verbose:
                    print(f"--- Venv dict does NOT contain packman = {packman}")
                continue

        if verbose:
            print('==== FINDING VIRTUAL ENVS DEPENDENCIES FINISHED ====')

    def get_some_dependencies(self, prompt_nested_lists=None, venvs=None, verbose=False):
        """
        Retrieves dependencies for specified virtual environments.

        Args:
        - prompt_nested_lists (list, optional): List of lists containing package manager and environment name pairs. Defaults to None.
        - venvs (dict, optional): Dictionary containing information about virtual environments. Defaults to None.
        - verbose (bool, optional): Verbosity flag. Defaults to False.

        Returns:
        - dict or False: A dictionary containing dependencies of specified virtual environments where keys are package manager names, and values are dictionaries of dependencies, or False if dependencies cannot be retrieved.
        """
        data_validated = True
        deps = {} # dict of dependencies

        if venvs is None or venvs == {}:
            if len(self.grouped_paths)>0:
                venvs = self.grouped_paths
            else:
                if verbose:
                    print("Vevs dict is empty. Use get_venvs_paths() + get_conda_envs() to fill it")
                return False

        if not isinstance(venvs, dict):
            if verbose:
                print("Invalid input argument. Please ensure venvs param is a dictionary.")
            data_validated = False
            return False

        if prompt_nested_lists is None or prompt_nested_lists == [[]]:
            prompt_nested_lists = [
                ['conda', 'myenv'],
                ['conda', 'base'],
                ['venv', 'myenv'],
                ['venv', 'base'],
                #['virtualenvs', 'Buratino']
            ]

        for sublist in prompt_nested_lists:
            if not (isinstance(sublist, list) and len(sublist) == 2):
                if verbose:
                    print("Invalid input argument. Please ensure your input prompt_nested_lists is a list of lists, with each sublist containing 2 elements.")
                data_validated = False
                return False

            packman, env_name = sublist

            if not isinstance(packman, str) and isinstance(env_name, str):
                if verbose:
                    print("Invalid input arguments. Please ensure each sublist of prompt_nested_lists contains a string name of packman and a string name of venv.")
                data_validated = False
                return False

        if data_validated:
            for pr in prompt_nested_lists:
                packman = pr[0]
                venv_name = pr[1]

                if verbose:
                    print("----------------------------------------------------------------------")
                    print(f"Getting dependencies for packman = {packman} | venv_name = {venv_name}")

                deps_geted = deps.get(packman, {}).get(venv_name)

                if deps_geted is None:
                    if verbose:
                        print("-- Dependencies not retrieved yet --")

                    if self.check_venv_founded(packman, venv_name, venvs, verbose):
                        if verbose:
                            print("Venv dict contains such data. Running get_dependencies().")
                        deps_geted = self.get_dependencies(packman, venv_name, venvs,verbose=verbose)

                        if deps_geted or deps_geted == {}:
                            if verbose:
                                print("--- Dependencies obtained! Updating deps dict ---")
                            deps.setdefault(packman, {})[venv_name] = deps_geted
                        else:
                            if verbose:
                                print("--- Dependencies NOT obtained ---")
                    else:
                        if verbose:
                            print("Venv dict does NOT contain such data.")
                else:
                    if verbose:
                        print("Dependencies for this packman and venv already retrieved.")

        return deps
    
    def run_autoshell_command(self, command, verbose=False):
        process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
        output, error = process.communicate()
        output = output.decode("utf-8")
        print(output)
        if error:
            self.errors[str(command)] = error
            if verbose:
                print("Error ocured at subprocess.Popen(..):",error)
        return output

    def get_base_win_paths(self, verbose=False):
        command = ["where", "python"]
        python_paths = self.run_autoshell_command(command).split('\n')

        # Фильтруем пути, исключая те, что содержат 'WindowsApps'
        python_paths = [path.strip() for path in python_paths if "WindowsApps" not in path]
        # Регулярное выражение для извлечения версии Python из пути
        version_pattern = re.compile(r"Python(\d+)(\d+)\\python.exe")

        for python_path in python_paths:
            if verbose:
                print("Получаем версии базовых питонов на пути:")
                print(python_path)
            # Извлекаем версию Python из пути
            version_match = version_pattern.search(python_path)
            if version_match:
                python_version = f"base_python{version_match.group(1)[0]}."+\
                    f"{version_match.group(1)[1:]}{version_match.group(2)}"
                self.grouped_paths['venv'][python_version] = python_path
                #python_version = f"Python{version_match.group(1)}.{version_match.group(2)}"
            else:
                continue

    def get_base_win_deps(self,env_name,verbose=False):
        python_path = self.check_venv_founded('venv', env_name, self.grouped_paths, verbose)
        if python_path:
            # Получаем список зависимостей для данного интерпретатора Python
            try:
                #command = f'"{python_path}" -m pip list --format=freeze'
                command = [str(python_path), '-m', 'pip', 'list', '--format=freeze']
                if verbose:
                    print(f"Attempting run command={command}")
                output = self.run_autoshell_command(command,verbose=verbose)
                if verbose:
                    print(f"command executed")
                dependencies_list = output.split('\n')
                dependencies = {item.split('==')[0]: item.split('==')[1] for item in dependencies_list if '==' in item}
                return dependencies
            except Exception as e:
                self.errors['deps_getting_for_'+str(command)]=e
                if verbose:
                    print(f"deps_getting error for path: {python_path}: {e}")
                return dependencies



if __name__ == '__main__':
    deps_getter = DepsGetter()
    print("Getting venvs paths...")
    deps_getter.get_venvs_paths(verbose=True)
    print("Getting conda env list...")
    deps_getter.get_conda_envs(verbose=True)
    print("---------------------------------------")
    print("Checked activate scripts paths:")
    deps_getter.da.print_dict(deps_getter.grouped_paths)
    print("---------------------------------------")
    print("Getting dependencies for some venvs...")
    prompt_nested_lists = [
                #['conda', 'myenv'],
                #['conda', 'base'],
                ['venv', 'myenv'],
                ['venv', 'base_python3.11'],
                ['venv', 'base_python3.9'],
                #['virtualenvs', 'Buratino']
            ]
    deps = deps_getter.get_some_dependencies(prompt_nested_lists=prompt_nested_lists,
                                             venvs=deps_getter.grouped_paths,
                                             verbose=True)
    print("---------------------------------------")
    print("- get_some_dependencies result ------")
    deps_getter.da.print_dict(deps)