import subprocess
import os
import sys

def run_commands_in_parallel(commands):
    """
    Выполняет список команд в отдельных процессах.

    Args:
      commands: Список строк, представляющих команды для выполнения.
    """
    processes = []
    for command in commands:
        process = subprocess.Popen(command, shell=True)
        processes.append(process)

    for process in processes:
        process.wait()

def get_project_dir():
    """Возвращает абсолютный путь к директории проекта."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

if __name__ == "__main__":

    project_dir = get_project_dir()
    fastapi_dir = os.path.join(project_dir, 'imei_api')
    aiogram_dir = os.path.join(project_dir, 'imei_api')
    
    fastapi_command = f'cd {fastapi_dir} && uvicorn api.main:app --reload'
    aiogram_command = f'cd {aiogram_dir} && python -m bot.main'

    commands = [fastapi_command, aiogram_command]

    run_commands_in_parallel(commands)
    print('Все процессы завершены')