import sys
import os
import subprocess
from environcheck import EnvironCheck
from envsfider import VenvsFinder
from mylog import MyLogger
from dictan import DictAnalyzer

envilog = MyLogger(name='ech',create_level='INFO',enable_logging=True)

da = DictAnalyzer(envilog,30)
venvsfinder = VenvsFinder(llev=30,envilog=envilog,verbose=False)
ech = EnvironCheck(llev=30,envilog=envilog,verbose=False)

envs_path_list_win = []
envs_path_list_linux = []

result_list = []
# Определение разделителя пути в зависимости от операционной системы
slash = '\\' if sys.platform == 'win32' else '/'
grouped_paths = {}
# Группировка путей для virtualenvs, conda, venv
grouped_paths['venv'] = {}
grouped_paths['virtualenvs'] = {}
grouped_paths['conda'] = {}

def get_venvs_paths(envs_path_list_win=None,
                    envs_path_list_linux=None):
    if sys.platform == 'win32':
        slash = '\\'
        home_path = os.environ['USERPROFILE']
        if envs_path_list_win is None \
            or envs_path_list_win==[]:
            envs_path_list_win = [
                home_path + '\\.virtualenvs',
                home_path + '\\anaconda3\\envs',
                home_path + '\\Documents\\pro',
                'C:\\Projects'
            ]
        
        for ptf in envs_path_list_win:
            print("Searching in:",ptf)
            res = venvsfinder.search_venvs_path(
                path_find=ptf, shell='powershell',verbose=False)
            if res != ['']:
                result_list.extend(res)
        
            for path in result_list:
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
                grouped_paths.setdefault(env_type, {}).update({env_name: path})

    if sys.platform.startswith('linux'):
        slash = '/'
        home_path = os.environ['HOME']
        if envs_path_list_linux is None \
            or envs_path_list_linux==[]:
            if ech.container_id:
                envs_path_list_linux = ["/"]
            else:
                envs_path_list_linux = [
                os.path.join(home_path, '.virtualenvs'),
                os.path.join(home_path, 'anaconda3', 'envs'),
                os.path.join(home_path, 'Documents', 'pro'),
                '/Projects'
            ]

        for ptf in envs_path_list_linux:
            res = venvsfinder.search_venvs_path(
                path_find=ptf, shell='bash',verbose=True)
            if res != ['']:
                result_list.extend(res)

        #print(result_list)
                
        # Группировка путей для базовых окружений
        for path in result_list:
            parts = path.split('/')
            if 'common' in parts:
                if 'conda' in path:
                    grouped_paths['conda']['base'] = [path]
                elif 'venv' in parts:
                    grouped_paths['venv']['base'] = path

            elif 'bin' in parts and 'activate' in parts \
                    and 'conda' not in parts \
                    and '.virtualenvs' not in parts:
                env_name = parts[-3]
                grouped_paths['venv'][env_name]=path
            elif 'bin' in parts and 'activate' in parts \
                    and 'conda' not in parts \
                    and '.virtualenvs' in parts:
                env_name = parts[-3]
                grouped_paths['virtualenv'][env_name]=path

def get_conda_envs():
    conda_envs = []
    try:
        # Проверяем, установлена ли Conda
        conda_check = subprocess.run(\
            ["conda", "--version"], capture_output=True, text=True)
        
        if conda_check.returncode != 0:
            print("Conda is not installed.")
            grouped_paths['conda'] = False
            return []
        else:
            print("Conda installed.")
        # Выполняем команду "conda env list" и декодируем вывод
        process = subprocess.Popen(
                            ["conda", "env", "list"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
        output, error = process.communicate()
        conda_list = output.decode("utf-8")
        #print(conda_list.split('\n')[1:])
        for line in conda_list.split('\n')[2:]:
            if line:
                #print(line.split())
                venv_info = line.split()
                if len(venv_info)>0:
                    venv_name = venv_info[0]
                    if len(venv_info)>1:
                        venv_path = venv_info[1]
                    else: venv_path = ''
                    grouped_paths['conda'][venv_name] = venv_path
                    conda_envs.append(venv_name)
        return conda_envs
    except Exception as e:
        print("Error during conda execution:",e)
        return conda_envs

def get_dependencies_conda(conda_env_name):
    command = ['conda', 'list', '-n',conda_env_name]
    process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                            )
    output, error = process.communicate()
    dependencies = output.decode("utf-8")
    packages = {}
    for line in dependencies.split('\n')[4:]:
        if line:
            package_info = line.split()
            package_name = package_info[0]
            package_version = package_info[1]
            packages[package_name] = package_version
    return packages

def check_venv_founded(package_manager, env_name, environments):
    path = environments.get(package_manager, {}).get(env_name)
    if path is None:
        print(f"Path for {package_manager} : {env_name} NOT found")
        return False
    elif path == '':
        print(f"Path for {package_manager} : {env_name} is empty")
        return False
    return path

def get_dependencies(package_manager, env_name, environments):
    dependencies = {}
    venv_path = check_venv_founded(package_manager, env_name, environments)
    if venv_path:
        if package_manager == 'conda':
            dependencies = get_dependencies_conda(env_name)
            return dependencies
        
        elif package_manager in ['virtualenvs','venv']:
            shell_path = None
            # Формируем команду для активации виртуального окружения
            if sys.platform.startswith('linux'):
                shell_path = os.environ.get('SHELL', '/bin/bash')
                command = f"source {venv_path} && pip list"
            
            if sys.platform == 'win32':
                shell_path = os.environ.get('COMSPEC', 'cmd.exe')
                print('win shell path:',shell_path)
                command = f"{venv_path} && pip list"

            print(command)
            # Выполняем команду через оболочку
            process = subprocess.Popen(command
                            , stdout=subprocess.PIPE
                            , stderr=subprocess.PIPE
                            , shell=True
                            , executable=shell_path
                            )
            output, error = process.communicate()
            
            
            dependencies = {}
            if output:
                output_str = output.decode("utf-8")
                lines = output_str.strip().split('\n')[2:]  # Пропускаем первые две строки
                for line in lines:
                    parts = line.split()
                    package_name = parts[0]
                    package_version = parts[1]
                    dependencies[package_name] = package_version
            return dependencies
    else:
        return False

def get_all_dependencies():
    for packman in [
        'virtualenvs',
        'conda',
        'venv'
        ]:
        print("---------------------------------------------------------")
        print(f"------{packman}------------")
        if packman in environments:
            for env_name in environments[packman]:
                print("env name:",env_name)
                if check_venv_founded(packman,env_name,environments):
                    dependencies = \
                    get_dependencies(packman,env_name,environments)
                    print(dependencies)
                else:
                    print(f"---Data for package manager: {packman} and venv: {env_name} not founded")
        else:
            print(f"---Data for package manager {packman} not founded")
    print('====FINDING VIRTUAL ENVS DEPENDENCIES FINISHED=====')


print("Geting venvs paths...")
# updating grouped_paths dict
get_venvs_paths(envs_path_list_win=None,envs_path_list_linux=None)

print("Geting conda env list...")
# updating grouped_paths dict
get_conda_envs()

da.print_dict(grouped_paths)
environments = grouped_paths

#get_all_dependencies()
print('-----geting conda myenv deps-----')
print(get_dependencies('conda','myenv',environments))

print('-----geting conda fastapi deps-----')
print(get_dependencies('conda','fastapi',environments))

print('-----geting venv myenv deps-----')
print(get_dependencies('venv','myenv',environments))

print('-----geting venv arch deps-----')
print(get_dependencies('venv','arch',environments))

print('-----geting virtualenv Buratino deps-----')
#print(environments['virtualenvs']['Buratino'])
print(get_dependencies('virtualenvs','Buratino',environments))


"""
# sample of environmets dict resulted as grouped_path
environments = \
{
'virtualenvs':
    {
        'Archip_Logging': 'C:\\Users\\user\\.virtualenvs\\Archip_Logging\\Scripts\\activate',
        'Archip_OOPushka': 'C:\\Users\\user\\.virtualenvs\\Archip_OOPushka\\Scripts\\activate',
        'Buratino': 'C:\\Users\\user\\.virtualenvs\\Buratino\\Scripts\\activate',
        'chicago_spark': 'C:\\Users\\user\\.virtualenvs\\chicago_spark\\Scripts\\activate',
        'DemoPyCharmProductive': 'C:\\Users\\user\\.virtualenvs\\DemoPyCharmProductive\\Scripts\\activate',
        'PapaPy': 'C:\\Users\\user\\.virtualenvs\\PapaPy\\Scripts\\activate',
        'PyCharmLearningProject': 'C:\\Users\\user\\.virtualenvs\\PyCharmLearningProject\\Scripts\\activate',
        'pycharm_Luchanos': 'C:\\Users\\user\\.virtualenvs\\pycharm_Luchanos\\Scripts\\activate',
        'pyhub': 'C:\\Users\\user\\.virtualenvs\\pyhub\\Scripts\\activate'
    },
'conda': 
    {
        'fastapi': 'C:\\Users\\user\\anaconda3\\envs\\fastapi\\Lib\\venv\\scripts\\common\\activate',
        'spark': 'C:\\Users\\user\\anaconda3\\envs\\spark\\Lib\\venv\\scripts\\common\\activate',
        'tf': 'C:\\Users\\user\\anaconda3\\envs\\tf\\Lib\\venv\\scripts\\common\\activate',
        'vbt': 'C:\\Users\\user\\anaconda3\\envs\\vbt\\Lib\\venv\\scripts\\common\\activate'},
'venv': 
    {
        '.test_venv': 'C:\\Users\\user\\Documents\\Pro\\Archip\\arch\\.test_venv\\Scripts\\activate',
        'myenv_prompt': 'C:\\Users\\user\\Documents\\Pro\\Archip\\arch\\myenv_prompt\\Scripts\\activate',
        'arch': 'C:\\Users\\user\\Documents\\Pro\\Archip\\arch\\Scripts\\activate'
    }
}
"""
