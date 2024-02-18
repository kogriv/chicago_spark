import sys
import os
from environcheck import EnvironCheck
from envsfider import VenvsFinder
from mylog import MyLogger

envilog = MyLogger(name='ech',create_level='INFO',enable_logging=True)

venvsfinder = VenvsFinder(llev=30,envilog=envilog,verbose=False)
ech = EnvironCheck(llev=30,envilog=envilog,verbose=False)

envs_path_list_win = []

# Определение разделителя пути в зависимости от операционной системы
slash = '\\' if sys.platform == 'win32' else '/'
result_list = []

if sys.platform == 'win32':
    slash = '\\'
    home_path = os.environ['USERPROFILE']
    envs_path_list_win = [
        home_path + '\\.virtualenvs',
        home_path + '\\anaconda3\\envs',
        home_path + '\\Documents\\pro',
        'C:\\Projects'
    ]
    
    for ptf in envs_path_list_win:
        res = venvsfinder.search_venvs_path(
            path_find=ptf, shell='powershell',verbose=True)
        if res != ['']:
            result_list.extend(res)


envs_path_list_linux = []

if sys.platform.startswith('linux'):
    slash = '\\'
    home_path = os.environ['HOME']
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


grouped_paths = {}

if ech.container_id:
    # Группировка путей для базовых окружений
    common_envs = {}
    for path in result_list:
        parts = path.split('/')
        package_manager = 'package_manager'
        python_version = 'python_version'
        if 'common' in parts:
            if 'conda' in path:
                package_manager = 'conda'
                for part in parts:
                    if 'python' in part:
                        python_version = part
            elif 'venv' in parts:
                package_manager = 'venv'
                for part in parts:
                    if 'python' in part:
                        python_version = part

            common_envs[f"{package_manager}_{python_version}"] = path

    if common_envs:
        grouped_paths['common'] = common_envs

    # Группировка путей для .virtualenvs, conda, venv
    grouped_paths['venv'] = {}
    grouped_paths['.virtualenvs'] = {}
    grouped_paths['conda'] = {}

    for path in result_list:
        parts = path.split('/')
        if 'bin' in parts and 'activate' in parts \
            and 'conda' not in parts \
            and '.virtualenvs' not in parts:
            env_name = parts[-3]
            grouped_paths['venv'][env_name]=path
else:
    for path in result_list:
        parts = path.split(slash)
        if '.virtualenvs' in parts:
            env_type = 'virtualenvs'
            env_name = parts[parts.index('.virtualenvs') + 1]
        elif 'anaconda3' in parts:
            env_type = 'conda'
            env_name = parts[parts.index('anaconda3') + 2]
        else:
            env_type = 'venv'
            env_name = parts[-3]
        grouped_paths.setdefault(env_type, {}).update({env_name: path})

print(grouped_paths)

def get_dependencies(package_manager, env_name, environments):
    if env_name in environments.get(package_manager, {}):
        activate_script = environments[package_manager][env_name]
        # Extracting dependencies from the activate script
        with open(activate_script, 'r') as f:
            lines = f.readlines()

        dependencies = []
        for line in lines:
            if 'export' in line:
                if '=' in line:
                    dependency = line.split('=')[1].strip()
                else:
                    dependency = line
                dependencies.append(dependency)

        return dependencies
    elif env_name in environments.get('common', {}):
        # Handling the case where env_name is in the common group
        activate_script = environments['common'][env_name]
        # Extracting dependencies from the activate script
        with open(activate_script, 'r') as f:
            lines = f.readlines()

        dependencies = []
        for line in lines:
            if 'export' in line:
                dependency = line.split('=')[1].strip()
                dependencies.append(dependency)

        return dependencies
    else:
        print(f"Environment '{env_name}' not found for package manager '{package_manager}'.")
        return []
"""
host_venvs = \
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
dependencies = \
get_dependencies('virtualenvs','chicago_spark',grouped_paths)
print(dependencies)