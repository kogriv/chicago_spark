import os
import subprocess
import json

#result = subprocess.run(\
#    ["echo", "Hello, subprocess!"], capture_output=True, text=True)

# result = subprocess.run(\
#    "echo Hello, subprocess!", capture_output=True, text=True, shell=True)

# command = ["python", "-c", 'print("Hello, subprocess!")']
# result = subprocess.run(command, capture_output=True, text=True)

# print(result.returncode)
# print(result.stdout)

envs_info = subprocess.check_output(\
            ["conda", "env", "list", "--json"]).decode("utf-8")
        # Преобразуем JSON-данные в словарь
envs_data = json.loads(envs_info)

print(envs_info)
print(envs_data)