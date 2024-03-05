import os
import shutil
import random
import platform
import subprocess
import sys
import PySimpleGUI as sg
import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variables
DEBUG_MODE = False
VERSION = "1.0.1 - Grape, stable"
BUILD_INFO = "Released on March 3, 2024"
GAMES_FOLDER = "games"
FILES_FOLDER = "files"

# Commands
def cmd_help():
  return ("Available Commands:\n"
          "help - Display Commands again\n"
          "ls - List current files in the directory\n"
          "cd <directory> - Change directory\n"
          "mkdir <directory_name> - Create directory\n"
          "touch <file_name> - Create a new file\n"
          "rm <file_name> - Remove a file\n"
          "cp <source> <destination> - Copy a file\n"
          "mv <source> <destination> - Move or rename a file\n"
          "pwd - Print current working directory\n"
          "clear - Clear the output\n"
          "snake - Play the Snake game\n"
          "guess - Play the Number Guessing game\n"
          "info - Display build information and version\n"
          "devtools - Developer tools\n"
          "ping <host> - Ping a host\n"
          "curl <url> - Retrieve a URL\n"
          "browser - Open the built-in browser\n"
          "cpu - Measure CPU-related stuff\n"
          "mem - Measure memory-related stuff\n"
          "disk - Measure disk space\n"
          "rp - Displays running processes."
          "cn - Create text note"
          "en - Edit text note"
          "dn - Delete text note"
          "ds - Display a text note")
  
def cmd_ls():
    files = os.listdir('.')
    return '\n'.join(files)

def cmd_cd(directory):
    try:
        os.chdir(directory)
        return f"Directory changed to: {directory}"
    except FileNotFoundError:
        return "Directory not found"

def cmd_mkdir(directory_name):
    try:
        os.mkdir(directory_name)
        return f"Directory created: {directory_name}"
    except FileExistsError:
        return "Directory already exists"

def cmd_touch(file_name):
    try:
        with open(file_name, 'w'):
            pass
        return f"File created: {file_name}"
    except Exception as e:
        return f"Error creating file: {str(e)}"

def cmd_rm(file_name):
    try:
        os.remove(file_name)
        return f"File removed: {file_name}"
    except FileNotFoundError:
        return "File not found"

def cmd_cp(source, destination):
    try:
        shutil.copy(source, destination)
        return f"File copied: {source} to {destination}"
    except Exception as e:
        return f"Error copying file: {str(e)}"

def cmd_mv(source, destination):
    try:
        shutil.move(source, destination)
        return f"File moved: {source} to {destination}"
    except Exception as e:
        return f"Error moving file: {str(e)}"

def cmd_pwd():
    return os.getcwd()

def cmd_clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return ""

def play_snake_game():
    # Snake game logic
    game_output = "Welcome to Snake!\n" \
                  "Use WASD keys to control the snake.\n" \
                  "Press Q to quit.\n"

    # Initialize game state
    width = 20
    height = 10
    snake = [(width // 2, height // 2)]
    direction = (0, 0)
    fruit = (random.randint(0, width - 1), random.randint(0, height - 1))
    score = 0

    while True:
        # Draw the game board
        for y in range(height):
            for x in range(width):
                if (x, y) in snake:
                    game_output += 'O '
                elif (x, y) == fruit:
                    game_output += '* '
                else:
                    game_output += '. '
            game_output += '\n'

        # Check for collision with fruit
        if snake[0] == fruit:
            score += 1
            fruit = (random.randint(0, width - 1), random.randint(0, height - 1))
        else:
            snake.pop()

        # Move the snake
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        # Check for collision with walls or itself
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height or head in snake[1:]:
            game_output += f"Game over! Your score: {score}"
            return game_output

def cmd_snake():
    return play_snake_game()

def cmd_guess():
    return "Number Guessing game will be launched."

def cmd_info():
    return f"FranchukOS Version: {VERSION}\n" \
           f"Build Information: {BUILD_INFO}\n" \
           "Additional Build Information:\n" \
           "Multiple systems running on Inferno V33.4145.900.2\n" \
           "Calvary support? No"

def cmd_devtools():
    return "Developer Tools:\n" \
           "debug - Toggle debug mode to enable/disable debugging features\n" \
           "advinfo - Display advanced system information such as OS version, hardware and more\n" \
           "logs - Display system logs for debugging purposes"

def toggle_debug_mode():
    global DEBUG_MODE
    DEBUG_MODE = not DEBUG_MODE
    if DEBUG_MODE:
        return "Debug mode turned on."
    else:
        return "Debug mode turned off."

def view_system_information():
    return f"System Information:\n" \
           f"OS: {platform.system()} {platform.release()}\n" \
           f"Machine: {platform.machine()}\n" \
           f"Processor: {platform.processor()}"

def view_system_logs():
    return "System logs:\n" \
           "No logs available in this version."

def view_advanced_info():
    return "Advanced System Information:\n" \
           f"OS Name: franchukOS American Honey\n" \
           f"OS Version: 0.9, stable\n" \
           f"OS Build: 202432RE\n" \
           f"franiumbits: unk.\n" \
           f"Processor: {platform.processor()}\n" \
           f"Machine Type: {platform.machine()}"

def cmd_ping(host):
    try:
        response = subprocess.run(['ping', host], capture_output=True, text=True)
        return response.stdout
    except Exception as e:
        return f"Error executing ping command: {str(e)}"

def cmd_curl(url):
    try:
        response = subprocess.run(['curl', url], capture_output=True, text=True)
        return response.stdout
    except Exception as e:
        return f"Error executing curl command: {str(e)}"

def cmd_browser():
    return "Built-in browser launched."



# Function to plot live CPU usage
def display_cpu_usage():
    layout = [
        [sg.Text("CPU Usage:", size=(20, 1)), sg.Text("", size=(10, 1), key='-CPU_USAGE-')],
        [sg.Button('Quit')]
    ]

    window = sg.Window('CPU Usage', layout)

    while True:
        event, _ = window.read(timeout=1000)  # Update every second
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        cpu_percent = psutil.cpu_percent()
        window['-CPU_USAGE-'].update(f"{cpu_percent:.2f}%")

    window.close()


# Function to display memory usage
def display_memory_usage():
    layout = [
        [sg.Text("Memory Usage:", size=(20, 1)), sg.Text("", size=(10, 1), key='-MEMORY_USAGE-')],
        [sg.Button('Quit')]
    ]

    window = sg.Window('Memory Usage', layout)

    while True:
        event, _ = window.read(timeout=1000)  # Update every second
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        memory_percent = psutil.virtual_memory().percent
        window['-MEMORY_USAGE-'].update(f"{memory_percent:.2f}%")

    window.close()


# Command to display disk usage statistics
def display_disk_usage():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_name = partition.device
        try:
            partition_usage = shutil.disk_usage(partition.mountpoint)
            total_space_gb = partition_usage.total / (1024 ** 3)  # Convert bytes to GB
            used_space_gb = partition_usage.used / (1024 ** 3)
            free_space_gb = partition_usage.free / (1024 ** 3)
            print(f"Partition: {partition_name}")
            print(f"Total Space: {total_space_gb:.2f} GB")
            print(f"Used Space: {used_space_gb:.2f} GB")
            print(f"Free Space: {free_space_gb:.2f} GB")
            print()
        except PermissionError:
            print(f"Unable to access disk usage information for {partition_name}")





# Function to display running processes (Task Manager)
def display_running_processes():
    layout = [
        [sg.Text("PID"), sg.Text("Name"), sg.Text("CPU %"), sg.Text("Memory %")],
        [sg.Text("-" * 30)]  # Separator line
    ]

    # Get running processes
    processes = psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
    for process in processes:
        layout.append([
            sg.Text(str(process.info['pid'])),
            sg.Text(process.info['name']),
            sg.Text(f"{process.info['cpu_percent']:.2f}"),
            sg.Text(f"{process.info['memory_percent']:.2f}")
        ])

    layout.append([sg.Button('Quit')])

    window = sg.Window('Task Manager', layout)

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

    window.close()


def create_note(note_name):
    try:
        with open(note_name, 'w') as file:
            file.write("")
        print(f"Note '{note_name}' created successfully.")
    except Exception as e:
        print(f"Error creating note: {str(e)}")

# Function to edit an existing note
def edit_note(note_name):
    try:
        with open(note_name, 'a') as file:
            file.write(input("Enter your note:\n") + '\n')
        print(f"Note '{note_name}' edited successfully.")
    except Exception as e:
        print(f"Error editing note: {str(e)}")

# Function to display the contents of a note
def display_note(note_name):
    try:
        with open(note_name, 'r') as file:
            print(f"Contents of '{note_name}':")
            print(file.read())
    except FileNotFoundError:
        print(f"Note '{note_name}' not found.")
    except Exception as e:
        print(f"Error displaying note: {str(e)}")

# Function to delete a note
def delete_note(note_name):
    try:
        os.remove(note_name)
        print(f"Note '{note_name}' deleted successfully.")
    except FileNotFoundError:
        print(f"Note '{note_name}' not found.")
    except Exception as e:
        print(f"Error deleting note: {str(e)}")  

# Command dictionary
commands = {
    "help": cmd_help,
    "ls": cmd_ls,
    "cd": cmd_cd,
    "mkdir": cmd_mkdir,
    "touch": cmd_touch,
    "rm": cmd_rm,
    "cp": cmd_cp,
    "mv": cmd_mv,
    "pwd": cmd_pwd,
    "clear": cmd_clear,
    "snake": cmd_snake,
    "guess": cmd_guess,
    "info": cmd_info,
    "devtools": cmd_devtools,
    "debug": toggle_debug_mode,
    "sysinfo": view_system_information,
    "logs": view_system_logs,
    "advinfo": view_advanced_info,
    "ping": cmd_ping,
    "curl": cmd_curl,
    "browser": cmd_browser,
    "cpu": display_cpu_usage,
    "mem": display_memory_usage,
    "disk": display_disk_usage,
    "rp": display_running_processes, 
    "cn": create_note,
    "en": edit_note,
    "dn": delete_note,
    "ds": display_note, 

}

# Define the layout for the GUI
layout = [
    [sg.Output(size=(80, 20), key='-OUTPUT-')],
    [sg.InputText(size=(70, 1), key='-INPUT-'), sg.Button('Enter'), sg.Button('Quit')],
]

# Create the window
window = sg.Window('FranchukOS', layout)

# Event loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    elif event == 'Enter':
        window['-OUTPUT-'].update('')  # Clear the output
        command = values['-INPUT-'].strip().split(maxsplit=1)
        if command[0] == "quit":
            break
        elif command[0] in commands:
            try:
                output = commands[command[0]](*command[1:])
                if output:
                    print(output)
            except Exception as e:
                print(f"Error executing command: {str(e)}")
        else:
            print("Command not found. Type 'help' for available commands.")

window.close()

