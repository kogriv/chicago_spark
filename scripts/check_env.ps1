# Проверка активированных окружений Conda
function Check-CondaEnvs {
    try {
        $envs = (conda env list --json | ConvertFrom-Json).envs
        $result = @()
        foreach ($env in $envs) {
            $envName = Split-Path $env -Leaf
            $isActive = if ($env:CONDA_DEFAULT_ENV -and $env:CONDA_DEFAULT_ENV -eq $envName) {"Yes"} else {"No"}
            $result += [PSCustomObject]@{
                Environment = $envName
                Manager = "Conda"
                IsActive = $isActive
            }
        }
        return $result
    } catch {
        return @()
    }
}

# Проверка активированного окружения venv
function Check-VenvEnv {
    $venvPath = $env:VIRTUAL_ENV
    if ($venvPath) {
        $envName = Split-Path $venvPath -Leaf
        $isActive = "Yes"
        return [PSCustomObject]@{
            Environment = $envName
            Manager = "venv"
            IsActive = $isActive
        }
    }
    return @()
}

# Функция для получения зависимостей из Conda окружения
function Get-CondaDependencies {
    param (
        [string]$envName
    )
    $currentEnv = $env:CONDA_DEFAULT_ENV
    conda activate $envName
    $dependencies = conda list --export
    if ($currentEnv) {
        conda activate $currentEnv
    } else {
        conda deactivate
    }
    $dependencies = $dependencies -split "\n"
    return $dependencies -join "`r`n"
}

# Функция для получения зависимостей из venv окружения
function Get-VenvDependencies {
    param (
        [string]$envPath
    )
    $currentVenv = $env:VIRTUAL_ENV
    & $envPath\Scripts\Activate
    $dependencies = pip list --format=freeze
    if ($currentVenv) {
        & $currentVenv\Scripts\Activate
    } else {
        deactivate
    }
    $dependencies = $dependencies -split "\n"
    return $dependencies -join "`r`n"
}

# Функция для записи зависимостей в файл
function Write-DependenciesToFile {
    param (
        [string]$envName,
        [string]$manager,
        [string]$dependencies
    )
    $fileName = "requirements_${manager}_${envName}.txt"
    $dependencies | Out-File -FilePath $fileName
}

# Функция для проверки окружений virtualenv
function Check-VirtualenvEnvs {
    # 
    $virtualenvsPath = "C:\Users\user\.virtualenvs"
    $dirs = Get-ChildItem -Path $virtualenvsPath -Directory

    $envs = @()
    foreach ($dir in $dirs) {
        $envPath = Join-Path $virtualenvsPath $dir.Name
        # Проверка наличия папки Scripts, что является признаком virtualenv
        if (Test-Path "$envPath\Scripts") {
            $envs += [PSCustomObject]@{
                Environment = $dir.Name
                Manager = "virtualenv"
                IsActive = if ($env:VIRTUAL_ENV -and $env:VIRTUAL_ENV -eq $envPath) {"Yes"} else {"No"}
            }
        }
    }
    return $envs
}

# Главная функция
function Main {
    Write-Host "INCEPTION..."

    $allEnvs = @()
    Write-Host "checking envs..."
    Write-Host "*******************************************"
    $allEnvs += Check-CondaEnvs
    $allEnvs += Check-VenvEnv
    $allEnvs += Check-VirtualenvEnvs

    # Если окружение 'base' активно, но не в списке, добавляем его
    if ($env:CONDA_DEFAULT_ENV -and $env:CONDA_DEFAULT_ENV -eq 'base') {
        $allEnvs += [PSCustomObject]@{
            Environment = 'base'
            Manager = "Conda"
            IsActive = "Yes"
        }
    }

    # Форматированный вывод таблицы соответствий
    $allEnvs | Format-Table -AutoSize
    Write-Host "*******************************************"
    Write-Host ""

    # Обработка активных окружений и запись файлов с зависимостями
    Write-Host "requirements file  for active envs updating..."
    Write-Host ""
    foreach ($env in $allEnvs) {
        if ($env.IsActive -eq "Yes") {
            $dependencies = $null
            if ($env.Manager -eq "Conda") {
                $dependencies = Get-CondaDependencies $env.Environment
            } elseif ($env.Manager -eq "venv") {
                $dependencies = Get-VenvDependencies $env:VIRTUAL_ENV
            }

            if ($dependencies) {
                Write-DependenciesToFile -envName $env.Environment -manager $env.Manager -dependencies $dependencies
            }
        }
    }
    Write-Host "envs checking finished..."
    Write-Host ""
}

# Выполнение главной функции
Main