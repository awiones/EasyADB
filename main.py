import os
import subprocess
import sys
import platform
import time

PLATFORM_TOOLS_PATH = r"platform-tools" 

def run_adb_command(command):
    try:
        result = subprocess.check_output([os.path.join(PLATFORM_TOOLS_PATH, 'adb'), command]).decode()
        return result
    except subprocess.CalledProcessError:
        return None

def get_device_info(adb_path, device_id):
    info = {}
    try:
        result = subprocess.run([adb_path, '-s', device_id, 'shell', 'dumpsys', 'battery'], capture_output=True, text=True, check=True)
        info['Battery Info'] = result.stdout.strip().split('\n')
    except subprocess.CalledProcessError as e:
        info['Error'] = str(e)
    return info

def list_adb_devices():
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    
    try:
        result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True, check=True)
        
        devices_output = result.stdout.strip().split('\n')[1:]
        devices = [line.split()[0] for line in devices_output if line]
        
        if not devices:
            print("No devices connected.")
            sys.exit()
        else:
            print("Connected devices:")
            for device in devices:
                print(f"\nDevice ID: {device}")
                info = get_device_info(adb_path, device)
                for key, value in info.items():
                    if key == 'Battery Info':
                        print(f"{key}:")
                        for line in value:
                            print(f"  {line}")
                    else:
                        print(f"{key}: {value}")

            input("\nPress Enter to continue to the device options...")
            os.system(f'python {os.path.join(os.path.dirname(__file__), "connected.py")}')
    
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running adb: {e}")
    except FileNotFoundError:
        print("ADB binary not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def display_banner():
    banner = """
 _____                   _    ____  ____  
| ____|__ _ ___ _   _   / \\  |  _ \\| __ ) 
|  _| / _` / __| | | | / _ \\ | | | |  _ \\ 
| |__| (_| \\__ \\ |_| |/ ___ \\| |_| | |_) |
|_____\\__,_|___/\\__, /_/   \\_\\____/|____/ 
                |___/                     
By: Awiones
    """
    print(banner)

def display_menu():
    clear_screen()
    display_banner()
    menu = """
[1] Device Management
[2] App Management
[3] File Management
[4] System Management
[5] Shell and Command Execution
[6] Screen Management
[7] Network Management
[8] Data Management
[9] Development and Testing
[10] Root Access and File Permissions
[11] Remote Control
[12] Power Management
[13] Permissions and Security
[14] Battery Management
[15] Advanced Usage
[0] Exit
    """
    print(menu)


def device_management():
    while True:
        clear_screen()
        display_banner()
        print("Device Management")
        menu = """
[1] Lists all the connected Android devices and emulators.
[2] Connects to a device over Wi-Fi.
[3] Disconnects from a device.
[4] Pairs a device with ADB over Wi-Fi (Android 11 and above).
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()
        
        if choice == "1":
            list_adb_devices()
            input("\nPress Enter to return to the Device Management menu...")
        elif choice == "2":
            connect_over_wifi()
        elif choice == "3":
            disconnect_device()
        elif choice == "4":
            pair_device_over_wifi()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def connect_over_wifi():
    clear_screen()
    print("Connect to a device over Wi-Fi")
    ip = input("Enter the device IP address: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'tcpip', '5555'], check=True)
        subprocess.run([adb_path, 'connect', ip], check=True)
        print(f"Successfully connected to {ip}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Device Management menu...")

def disconnect_device():
    clear_screen()
    print("Disconnect a device")
    ip = input("Enter the device IP address to disconnect: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'disconnect', ip], check=True)
        print(f"Successfully disconnected from {ip}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Device Management menu...")

def pair_device_over_wifi():
    clear_screen()
    print("Pair a device with ADB over Wi-Fi (Android 11 and above)")
    ip = input("Enter the device IP address: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'pair', ip], check=True)
        print(f"Successfully paired with {ip}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Device Management menu...")

def app_management():
    while True:
        clear_screen()
        display_banner()
        print("App Management")
        menu = """
[1] Install an APK file.
[2] Uninstall an app.
[3] Install multiple APKs.
[4] Reinstall an app, keeping its data.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            install_apk()
        elif choice == "2":
            uninstall_app()
        elif choice == "3":
            install_multiple_apks()
        elif choice == "4":
            reinstall_apk()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def install_apk():
    clear_screen()
    print("Install APK")
    apk_path = input("Enter the path to the APK file: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'install', apk_path], check=True)
        print("APK installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the App Management menu...")

def uninstall_app():
    clear_screen()
    print("Uninstall App")
    package_name = input("Enter the package name of the app to uninstall: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'uninstall', package_name], check=True)
        print("App uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the App Management menu...")

def install_multiple_apks():
    clear_screen()
    print("Install Multiple APKs")
    apks = input("Enter the paths to the APK files separated by spaces: ").strip().split()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'install-multiple'] + apks, check=True)
        print("Multiple APKs installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the App Management menu...")

def reinstall_apk():
    clear_screen()
    print("Reinstall APK")
    apk_path = input("Enter the path to the APK file: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'install', '-r', apk_path], check=True)
        print("APK reinstalled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the App Management menu...")


def file_management():
    while True:
        clear_screen()
        display_banner()
        print("File Management")
        menu = """
[1] Push a file to the device.
[2] Pull a file from the device.
[3] Delete a file on the device.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            push_file()
        elif choice == "2":
            pull_file()
        elif choice == "3":
            delete_file()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def push_file():
    clear_screen()
    print("Push File to Device")
    local_path = input("Enter the local file path: ").strip()
    remote_path = input("Enter the remote path on the device: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'push', local_path, remote_path], check=True)
        print("File pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the File Management menu...")

def pull_file():
    clear_screen()
    print("Pull File from Device")
    remote_path = input("Enter the remote file path on the device: ").strip()
    local_path = input("Enter the local path to save the file: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'pull', remote_path, local_path], check=True)
        print("File pulled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the File Management menu...")

def delete_file():
    clear_screen()
    print("Delete File on Device")
    remote_path = input("Enter the remote file path on the device to delete: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'rm', remote_path], check=True)
        print("File deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the File Management menu...")


def system_management():
    while True:
        clear_screen()
        display_banner()
        print("System Management")
        menu = """
[1] Stream system logs.
[2] Save logs to a file.
[3] Generate a bug report.
[4] Dump system service information.
[5] Display real-time system processes.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            stream_logs()
        elif choice == "2":
            save_logs_to_file()
        elif choice == "3":
            generate_bug_report()
        elif choice == "4":
            dump_system_service_info()
        elif choice == "5":
            display_system_processes()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def stream_logs():
    clear_screen()
    print("Streaming System Logs")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'logcat'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the System Management menu...")

def save_logs_to_file():
    clear_screen()
    print("Saving Logs to File")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        with open('logcat.txt', 'w') as log_file:
            subprocess.run([adb_path, 'logcat', '-d'], stdout=log_file, check=True)
        print("Logs saved to logcat.txt.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the System Management menu...")

def generate_bug_report():
    clear_screen()
    print("Generating Bug Report")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'bugreport'], check=True)
        print("Bug report generated.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the System Management menu...")

def dump_system_service_info():
    clear_screen()
    print("Dumping System Service Information")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'dumpsys'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the System Management menu...")

def display_system_processes():
    clear_screen()
    print("Displaying Real-Time System Processes")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'top'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the System Management menu...")

def shell_and_command_execution():
    while True:
        clear_screen()
        display_banner()
        print("Shell and Command Execution")
        menu = """
[1] Start an interactive shell on the device.
[2] Run a specific command on the device's shell.
[3] List all installed packages on the device.
[4] Uninstall a package via shell.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            start_interactive_shell()
        elif choice == "2":
            run_specific_command()
        elif choice == "3":
            list_installed_packages()
        elif choice == "4":
            uninstall_package()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def start_interactive_shell():
    clear_screen()
    print("Starting Interactive Shell")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Shell and Command Execution menu...")

def run_specific_command():
    clear_screen()
    print("Run a Specific Command")
    command = input("Enter the command to run: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        result = subprocess.check_output([adb_path, 'shell'] + command.split()).decode()
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Shell and Command Execution menu...")

def list_installed_packages():
    clear_screen()
    print("Listing Installed Packages")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        result = subprocess.check_output([adb_path, 'shell', 'pm', 'list', 'packages']).decode()
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Shell and Command Execution menu...")

def uninstall_package():
    clear_screen()
    print("Uninstall a Package")
    package_name = input("Enter the package name to uninstall: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'pm', 'uninstall', package_name], check=True)
        print(f"Package {package_name} has been uninstalled.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Shell and Command Execution menu...")

def screen_management():
    while True:
        clear_screen()
        display_banner()
        print("Screen Management")
        menu = """
[1] Take a screenshot of the device screen.
[2] Record the screen to a video file.
[3] Get or set the screen resolution.
[4] Get or set the screen density.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            take_screenshot()
        elif choice == "2":
            record_screen()
        elif choice == "3":
            manage_screen_resolution()
        elif choice == "4":
            manage_screen_density()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def take_screenshot():
    clear_screen()
    print("Taking a Screenshot")
    filename = input("Enter the filename to save the screenshot: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'screencap', '/sdcard/' + filename], check=True)
        subprocess.run([adb_path, 'pull', '/sdcard/' + filename, filename], check=True)
        print(f"Screenshot saved as {filename}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Screen Management menu...")

def record_screen():
    clear_screen()
    print("Recording the Screen")
    filename = input("Enter the filename to save the video: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'screenrecord', '/sdcard/' + filename], check=True)
        subprocess.run([adb_path, 'pull', '/sdcard/' + filename, filename], check=True)
        print(f"Screen recording saved as {filename}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Screen Management menu...")

def manage_screen_resolution():
    clear_screen()
    print("Get or Set Screen Resolution")
    action = input("Enter 'get' to get the resolution or 'set' to set a new resolution: ").strip().lower()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    if action == 'get':
        try:
            result = subprocess.check_output([adb_path, 'shell', 'wm', 'size']).decode()
            print(result)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    elif action == 'set':
        new_resolution = input("Enter the new resolution (e.g., 1080x1920): ").strip()
        try:
            subprocess.run([adb_path, 'shell', 'wm', 'size', new_resolution], check=True)
            print(f"Screen resolution set to {new_resolution}.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        print("Invalid option.")
    input("\nPress Enter to return to the Screen Management menu...")

def manage_screen_density():
    clear_screen()
    print("Get or Set Screen Density")
    action = input("Enter 'get' to get the density or 'set' to set a new density: ").strip().lower()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    if action == 'get':
        try:
            result = subprocess.check_output([adb_path, 'shell', 'wm', 'density']).decode()
            print(result)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    elif action == 'set':
        new_density = input("Enter the new density (e.g., 320): ").strip()
        try:
            subprocess.run([adb_path, 'shell', 'wm', 'density', new_density], check=True)
            print(f"Screen density set to {new_density}.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        print("Invalid option.")
    input("\nPress Enter to return to the Screen Management menu...")

def network_management():
    while True:
        clear_screen()
        display_banner()
        print("Network Management")
        menu = """
[1] Forward a local port to a remote port on the device.
[2] Forward a remote port to a local port.
[3] Display network interface configurations.
[4] Enable or disable airplane mode.
[5] Enable or disable Wi-Fi.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            forward_local_to_remote()
        elif choice == "2":
            forward_remote_to_local()
        elif choice == "3":
            display_network_configurations()
        elif choice == "4":
            toggle_airplane_mode()
        elif choice == "5":
            toggle_wifi()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def forward_local_to_remote():
    clear_screen()
    print("Forwarding Local Port to Remote Port")
    local_port = input("Enter the local port: ").strip()
    remote_port = input("Enter the remote port: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'forward', f'tcp:{local_port}', f'tcp:{remote_port}'], check=True)
        print(f"Local port {local_port} forwarded to remote port {remote_port}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Network Management menu...")

def forward_remote_to_local():
    clear_screen()
    print("Forwarding Remote Port to Local Port")
    remote_port = input("Enter the remote port: ").strip()
    local_port = input("Enter the local port: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'reverse', f'tcp:{remote_port}', f'tcp:{local_port}'], check=True)
        print(f"Remote port {remote_port} forwarded to local port {local_port}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Network Management menu...")

def display_network_configurations():
    clear_screen()
    print("Displaying Network Interface Configurations")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        result = subprocess.check_output([adb_path, 'shell', 'netcfg']).decode()
        print(result)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Network Management menu...")

def toggle_airplane_mode():
    clear_screen()
    print("Toggle Airplane Mode")
    action = input("Enter 'enable' to enable or 'disable' to disable airplane mode: ").strip().lower()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    if action == 'enable':
        try:
            subprocess.run([adb_path, 'shell', 'settings', 'put', 'global', 'airplane_mode_on', '1'], check=True)
            print("Airplane mode enabled.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    elif action == 'disable':
        try:
            subprocess.run([adb_path, 'shell', 'settings', 'put', 'global', 'airplane_mode_on', '0'], check=True)
            print("Airplane mode disabled.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        print("Invalid option.")
    input("\nPress Enter to return to the Network Management menu...")

def toggle_wifi():
    clear_screen()
    print("Toggle Wi-Fi")
    action = input("Enter 'enable' to enable or 'disable' to disable Wi-Fi: ").strip().lower()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    if action == 'enable':
        try:
            subprocess.run([adb_path, 'shell', 'svc', 'wifi', 'enable'], check=True)
            print("Wi-Fi enabled.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    elif action == 'disable':
        try:
            subprocess.run([adb_path, 'shell', 'svc', 'wifi', 'disable'], check=True)
            print("Wi-Fi disabled.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    else:
        print("Invalid option.")
    input("\nPress Enter to return to the Network Management menu...")

def data_management():
    while True:
        clear_screen()
        display_banner()
        print("Data Management")
        menu = """
[1] Create a full backup of the device.
[2] Restore a backup to the device.
[3] Clear app data for a specified package.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            create_backup()
        elif choice == "2":
            restore_backup()
        elif choice == "3":
            clear_app_data()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def create_backup():
    clear_screen()
    print("Creating a Full Backup")
    filename = input("Enter the filename to save the backup: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'backup', '-f', filename, '-apk', '-shared', '-all'], check=True)
        print(f"Backup saved as {filename}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Data Management menu...")

def restore_backup():
    clear_screen()
    print("Restoring a Backup")
    filename = input("Enter the filename of the backup to restore: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'restore', filename], check=True)
        print(f"Backup {filename} restored.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Data Management menu...")

def clear_app_data():
    clear_screen()
    print("Clearing App Data")
    package_name = input("Enter the package name of the app to clear data for: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'am', 'clear', package_name], check=True)
        print(f"App data for {package_name} cleared.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Data Management menu...")

def development_testing():
    while True:
        clear_screen()
        display_banner()
        print("Development and Testing")
        menu = """
[1] Run a stress test using monkey.
[2] Start an activity.
[3] Simulate user input.
[4] Manage device settings.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            run_monkey_test()
        elif choice == "2":
            start_activity()
        elif choice == "3":
            simulate_user_input()
        elif choice == "4":
            manage_device_settings()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def run_monkey_test():
    clear_screen()
    print("Running Monkey Stress Test")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'monkey', '-v', '500'], check=True)
        print("Monkey test completed.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Development and Testing menu...")

def start_activity():
    clear_screen()
    print("Starting Activity")
    component = input("Enter the component name (e.g., com.example/.MainActivity): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'am', 'start', '-n', component], check=True)
        print(f"Activity {component} started.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Development and Testing menu...")

def simulate_user_input():
    clear_screen()
    print("Simulating User Input")
    command = input("Enter the input command (e.g., tap, swipe, text): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'input', command], check=True)
        print(f"Simulated input command: {command}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Development and Testing menu...")

def manage_device_settings():
    clear_screen()
    print("Managing Device Settings")
    command = input("Enter the settings command (e.g., settings put global <key> <value>): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'settings'] + command.split(), check=True)
        print(f"Executed settings command: {command}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Development and Testing menu...")

def root_access_permissions():
    while True:
        clear_screen()
        display_banner()
        print("Root Access and File Permissions")
        menu = """
[1] Restart adbd daemon with root privileges.
[2] Restart adbd daemon without root privileges.
[3] Remount the system partitions as writable.
[4] Change file permissions.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            restart_adbd_root()
        elif choice == "2":
            restart_adbd_unroot()
        elif choice == "3":
            remount_system_partitions()
        elif choice == "4":
            change_file_permissions()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def restart_adbd_root():
    clear_screen()
    print("Restarting adbd with root privileges")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'root'], check=True)
        print("adbd daemon restarted with root privileges.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Root Access and File Permissions menu...")

def restart_adbd_unroot():
    clear_screen()
    print("Restarting adbd without root privileges")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'unroot'], check=True)
        print("adbd daemon restarted without root privileges.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Root Access and File Permissions menu...")

def remount_system_partitions():
    clear_screen()
    print("Remounting system partitions as writable")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'remount'], check=True)
        print("System partitions remounted as writable.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Root Access and File Permissions menu...")

def change_file_permissions():
    clear_screen()
    print("Changing File Permissions")
    file_path = input("Enter the file path on the device: ").strip()
    permissions = input("Enter the new permissions (e.g., 755): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'chmod', permissions, file_path], check=True)
        print(f"Permissions for {file_path} changed to {permissions}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Root Access and File Permissions menu...")

def remote_control():
    while True:
        clear_screen()
        display_banner()
        print("Remote Control")
        menu = """
[1] Send a key event.
[2] Simulate a tap at specified coordinates.
[3] Simulate a swipe.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            send_key_event()
        elif choice == "2":
            simulate_tap()
        elif choice == "3":
            simulate_swipe()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def send_key_event():
    clear_screen()
    print("Sending Key Event")
    keycode = input("Enter the keycode (e.g., 3 for Home, 4 for Back): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'input', 'keyevent', keycode], check=True)
        print(f"Key event {keycode} sent.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Remote Control menu...")

def simulate_tap():
    clear_screen()
    print("Simulating Tap")
    x = input("Enter the x-coordinate: ").strip()
    y = input("Enter the y-coordinate: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'input', 'tap', x, y], check=True)
        print(f"Tap simulated at coordinates ({x}, {y}).")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Remote Control menu...")

def simulate_swipe():
    clear_screen()
    print("Simulating Swipe")
    x1 = input("Enter the start x-coordinate: ").strip()
    y1 = input("Enter the start y-coordinate: ").strip()
    x2 = input("Enter the end x-coordinate: ").strip()
    y2 = input("Enter the end y-coordinate: ").strip()
    duration = input("Enter the swipe duration in milliseconds: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'input', 'swipe', x1, y1, x2, y2, duration], check=True)
        print(f"Swipe simulated from ({x1}, {y1}) to ({x2}, {y2}) over {duration} ms.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Remote Control menu...")

def power_management():
    while True:
        clear_screen()
        display_banner()
        print("Power Management")
        menu = """
[1] Reboot the device.
[2] Reboot the device into bootloader.
[3] Reboot the device into recovery mode.
[4] Power off the device.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            reboot_device()
        elif choice == "2":
            reboot_bootloader()
        elif choice == "3":
            reboot_recovery()
        elif choice == "4":
            power_off_device()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def reboot_device():
    clear_screen()
    print("Rebooting Device")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'reboot'], check=True)
        print("Device is rebooting.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Power Management menu...")

def reboot_bootloader():
    clear_screen()
    print("Rebooting Device into Bootloader")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'reboot', 'bootloader'], check=True)
        print("Device is rebooting into bootloader.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Power Management menu...")

def reboot_recovery():
    clear_screen()
    print("Rebooting Device into Recovery Mode")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'reboot', 'recovery'], check=True)
        print("Device is rebooting into recovery mode.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Power Management menu...")

def power_off_device():
    clear_screen()
    print("Powering Off Device")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'reboot', '-p'], check=True)
        print("Device is powering off.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Power Management menu...")

def permissions_security():
    while True:
        clear_screen()
        display_banner()
        print("Permissions and Security")
        menu = """
[1] Grant a specific permission to an app.
[2] Revoke a specific permission from an app.
[3] Manage device policies.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            grant_permission()
        elif choice == "2":
            revoke_permission()
        elif choice == "3":
            manage_device_policies()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def grant_permission():
    clear_screen()
    print("Granting Permission")
    package = input("Enter the package name: ").strip()
    permission = input("Enter the permission (e.g., android.permission.CAMERA): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'pm', 'grant', package, permission], check=True)
        print(f"Permission {permission} granted to {package}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Permissions and Security menu...")

def revoke_permission():
    clear_screen()
    print("Revoking Permission")
    package = input("Enter the package name: ").strip()
    permission = input("Enter the permission (e.g., android.permission.CAMERA): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'pm', 'revoke', package, permission], check=True)
        print(f"Permission {permission} revoked from {package}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Permissions and Security menu...")

def manage_device_policies():
    clear_screen()
    print("Managing Device Policies")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        # Attempt to run the device policy manager command
        result = subprocess.run([adb_path, 'shell', 'device_policy_manager'], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # Specific handling for command not found or inaccessible
        if 'not found' in e.stderr or 'inaccessible' in e.stderr:
            print("The 'device_policy_manager' command is not available on this device.")
            print("Possible reasons:")
            print("- The device may not support this command.")
            print("- The device may need to be rooted to access this feature.")
            print("- The command may require a different syntax or different device policies.")
        else:
            print(f"Error occurred: {e}")
    except FileNotFoundError:
        print("ADB binary not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("\nPress Enter to return to the Permissions and Security menu...")




def battery_management():
    while True:
        clear_screen()
        display_banner()
        print("Battery Management")
        menu = """
[1] Dump the current battery status.
[2] Set the battery level (useful for testing).
[3] Reset the battery status.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            dump_battery_status()
        elif choice == "2":
            set_battery_level()
        elif choice == "3":
            reset_battery_status()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def dump_battery_status():
    clear_screen()
    print("Dumping Battery Status")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        result = subprocess.run([adb_path, 'shell', 'dumpsys', 'battery'], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Battery Management menu...")

def set_battery_level():
    clear_screen()
    print("Setting Battery Level")
    level = input("Enter the battery level (e.g., 50): ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'dumpsys', 'battery', 'set', 'level', level], check=True)
        print(f"Battery level set to {level}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Battery Management menu...")

def reset_battery_status():
    clear_screen()
    print("Resetting Battery Status")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'dumpsys', 'battery', 'reset'], check=True)
        print("Battery status reset.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Battery Management menu...")

def advanced_usage():
    while True:
        clear_screen()
        display_banner()
        print("Advanced Usage")
        menu = """
[1] Wait for device connection.
[2] Enter superuser mode.
[3] Get device properties.
[4] Set device properties.
[0] Return to the main menu.
        """
        print(menu)
        choice = input("Select an option: ").strip()

        if choice == "1":
            wait_for_device()
        elif choice == "2":
            enter_superuser_mode()
        elif choice == "3":
            get_device_properties()
        elif choice == "4":
            set_device_properties()
        elif choice == "0":
            break
        else:
            print("Invalid option, please select again.")

def wait_for_device():
    clear_screen()
    print("Waiting for Device Connection")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'wait-for-device'], check=True)
        print("Device is now connected.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Advanced Usage menu...")

def enter_superuser_mode():
    clear_screen()
    print("Entering Superuser Mode")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'su'], check=True)
        print("Entered superuser mode.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Advanced Usage menu...")

def get_device_properties():
    clear_screen()
    print("Getting Device Properties")
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        result = subprocess.run([adb_path, 'shell', 'getprop'], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Advanced Usage menu...")

def set_device_properties():
    clear_screen()
    print("Setting Device Properties")
    prop_name = input("Enter the property name (e.g., sys.debuggable): ").strip()
    prop_value = input("Enter the property value: ").strip()
    adb_binary = 'adb' if platform.system() != 'Windows' else 'adb.exe'
    adb_path = os.path.join(PLATFORM_TOOLS_PATH, adb_binary)
    try:
        subprocess.run([adb_path, 'shell', 'setprop', prop_name, prop_value], check=True)
        print(f"Property {prop_name} set to {prop_value}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    input("\nPress Enter to return to the Advanced Usage menu...")


def exit_program():
    clear_screen()
    print("Exiting EasyADB.")
    sys.exit()

# Main function
def main():
    display_banner()
    list_adb_devices()

    while True:
        display_menu()
        choice = input("Select an option: ").strip()
        if choice == "1":
            device_management()
        elif choice == "2":
            app_management()
        elif choice == "3":
            file_management()
        elif choice == "4":
            system_management()
        elif choice == "5":
            shell_and_command_execution()
        elif choice == "6":
            screen_management()
        elif choice == "7":
            network_management()
        elif choice == "8":
            data_management()
        elif choice == "9":
            development_testing()
        elif choice == "10":
            root_access_permissions()
        elif choice == "11":
            remote_control()
        elif choice == "12":
            power_management()
        elif choice == "13":
            permissions_security()
        elif choice == "14":
            battery_management()
        elif choice == "15":
            advanced_usage()
        elif choice == "0":
            exit_program()
        else:
            print("Invalid option, please select again.")

if __name__ == "__main__":
    main()