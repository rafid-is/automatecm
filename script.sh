#!/bin/bash

# color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
WHITE='\033[1;35m]'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

#random system tip
display_random_tip() {
    local tips=(
        "Use 'Ctrl + C' to stop a running command in the terminal."
        "Run 'man <command>' to learn more about any command."
        "Use 'sudo !!' to rerun the last command with sudo."
        "Press 'Tab' for command or file name autocompletion."
        "Use 'history' to see your command history."
        "Clear your terminal with 'Ctrl + L' for a clean view."
        "Use 'grep' to search through command output easily."
        "Run 'df -h' to check disk space in a human-readable format."
        "Use 'top' or 'htop' for a live view of system processes."
        "Add '2>/dev/null' to suppress error messages in scripts."
    )
    local tip=${tips[$RANDOM % ${#tips[@]}]}
    echo -e "${CYAN}Tip: $tip${NC}"
}

# available commands lsit:
display_commands() {
    echo -e "${BLUE}Available commands:${NC}"
    echo "1) update_system - Update system packages"
    echo "2) upgrade_system - Upgrade system packages"
    echo "3) clean_cache - Clean package cache"
    echo "4) list_files - List files in current directory"
    echo "5) disk_usage - Show disk usage"
    echo "6) free_memory - Show free memory"
    echo "7) running_processes - List running processes"
    echo "8) check_cpu - Show CPU usage"
    echo "9) check_uptime - Show system uptime"
    echo "10) list_users - List all users"
    echo "11) check_date - Show current date and time"
    echo "12) network_info - Show network interfaces"
    echo "13) check_services - List active services"
    echo "14) restart_network - Restart network service"
    echo "15) check_logs - Show recent system logs"
    echo "16) disk_space - Show disk space usage"
    echo "17) list_cron - List cron jobs"
    echo "18) check_ports - Show open ports"
    echo "19) system_info - Show system information"
    echo "20) check_updates - Check for available updates"
    echo "21) clear_screen - Clear the terminal screen"
    echo "22) check_connectivity - Ping google.com to check connectivity"
    echo -e "${YELLOW}0) exit - Exit the script${NC}"
}

#function to execute a command and log results
execute_command() {
    local cmd=$1
    local desc=$2
    echo -e "${BLUE}Executing: $desc${NC}"
    # Run the command and capture output
    if $cmd > command_output.txt 2>&1; then
        echo -e "${GREEN}Command '$desc' executed successfully${NC}"
        log_result "$desc" "SUCCESS"
        cat command_output.txt
        return 0
    else
        echo -e "${RED}Command '$desc' failed${NC}"
        log_result "$desc" "FAILED"
        cat command_output.txt
        return 1
    fi
}

# function to log results to a file:
log_result() {
    local cmd=$1
    local status=$2
    local log_file="system_automation_log.txt"
    echo "[$(date)] [$status] Command: $cmd" >> "$log_file"
}

# Main script
echo -e "${GREEN}Starting interactive automation script...${NC}"

# Initialize counter for executed commands
command_count=0

# Main loop to keep prompting for commands:
while true; do
    # display available commands
    display_commands
    echo -n "Enter command number (0 to exit): "
    read choice
    # Conditional to handle user input
    case $choice in
        1)
            execute_command "sudo apt update" "update_system"
            ((command_count++))
            display_random_tip
            ;;
        2)
            execute_command "sudo apt upgrade -y" "upgrade_system"
            ((command_count++))
            display_random_tip
            ;;
        3)
            execute_command "sudo apt autoclean" "clean_cache"
            ((command_count++))
            display_random_tip
            ;;
        4)
            execute_command "ls -l" "list_files"
            ((command_count++))
            display_random_tip
            ;;
        5)
            execute_command "df -h" "disk_usage"
            ((command_count++))
            display_random_tip
            ;;
        6)
            execute_command "free -m" "free_memory"
            ((command_count++))
            display_random_tip
            ;;
        7)
            execute_command "ps aux" "running_processes"
            ((command_count++))
            display_random_tip
            ;;
        8)
            execute_command "top -bn1 | head -n 5" "check_cpu"
            ((command_count++))
            display_random_tip
            ;;
        9)
            execute_command "uptime" "check_uptime"
            ((command_count++))
            display_random_tip
            ;;
        10)
            execute_command "cat /etc/passwd | cut -d: -f1" "list_users"
            ((command_count++))
            display_random_tip
            ;;
        11)
            execute_command "date" "check_date"
            ((command_count++))
            display_random_tip
            ;;
        12)
            execute_command "ifconfig" "network_info"
            ((command_count++))
            display_random_tip
            ;;
        13)
            execute_command "systemctl list-units --type=service --state=active" "check_services"
            ((command_count++))
            display_random_tip
            ;;
        14)
            execute_command "sudo systemctl restart networking" "restart_network"
            ((command_count++))
            display_random_tip
            ;;
        15)
            execute_command "journalctl -n 10" "check_logs"
            ((command_count++))
            display_random_tip
            ;;
        16)
            execute_command "du -sh ." "disk_space"
            ((command_count++))
            display_random_tip
            ;;
        17)
            execute_command "crontab -l" "list_cron"
            ((command_count++))
            display_random_tip
            ;;
        18)
            execute_command "netstat -tuln" "check_ports"
            ((command_count++))
            display_random_tip
            ;;
        19)
            execute_command "uname -a" "system_info"
            ((command_count++))
            display_random_tip
            ;;
        20)
            execute_command "apt list --upgradable" "check_updates"
            ((command_count++))
            display_random_tip
            ;;
        21)
            execute_command "clear" "clear_screen"
            ((command_count++))
            display_random_tip
            ;;
        22)
            execute_command "ping -c 4 google.com" "check_connectivity"
            ((command_count++))
            display_random_tip
            ;;
        0)
            echo -e "${GREEN}Exiting script. Executed $command_count commands.${NC}"
            echo "Results logged to system_automation_log.txt"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please select a number between 0 and 22.${NC}"
            display_random_tip
            ;;
    esac
    echo ""
done
# finished
