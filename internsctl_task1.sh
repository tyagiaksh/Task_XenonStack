#!/bin/bash

# internsctl - Custom Linux Command for Operations
# Version: v0.1.0

function show_help() {
    echo "Usage: internsctl [OPTIONS]"
    echo "Custom Linux Command for Operations."
    echo
    echo "Options:"
    echo "  --help                   Display this help message"
    echo "  --version                Display command version"
    echo "  cpu getinfo              Get CPU information (similar to lscpu)"
    echo "  memory getinfo           Get memory information (similar to free)"
    echo "  user create <username>   Create a new user"
    echo "  user list                List all regular users"
    echo "  user list --sudo-only    List users with sudo permissions"
    echo "  file getinfo <file-name> Get information about a file"
    echo "                           Options:"
    echo "                             --size, -s            Print file size"
    echo "                             --permissions, -p     Print file permissions"
    echo "                             --owner, -o           Print file owner"
    echo "                             --last-modified, -m   Print last modified time"
    echo
    echo "Examples:"
    echo "  ./internsctl.sh --help"
    echo "  ./internsctl.sh --version"
    echo "  ./internsctl.sh cpu getinfo"
    echo "  ./internsctl.sh memory getinfo"
    echo "  ./internsctl.sh user create john_doe"
    echo "  ./internsctl.sh user list"
    echo "  ./internsctl.sh user list --sudo-only"
    echo "  ./internsctl.sh file getinfo hello.txt"
    echo "  ./internsctl.sh file getinfo --size hello.txt"
    echo "  ./internsctl.sh file getinfo --permissions hello.txt"
    echo "  ./internsctl.sh file getinfo --owner hello.txt"
    echo "  ./internsctl.sh file getinfo --last-modified hello.txt"
    echo
}

function show_version() {
    echo "internsctl v0.1.0"
}

function get_cpu_info() {
    lscpu
}

function get_memory_info() {
    free
}

function create_user() {
    if [ -z "$2" ]; then
        echo "Error: Missing username. Usage: internsctl user create <username>"
        exit 1
    fi

    sudo useradd -m "$2"
    echo "User '$2' created successfully."
}

function list_users() {
    if [ "$2" = "--sudo-only" ]; then
        getent passwd | grep -E 'sudo|admin' | cut -d: -f1
    else
        getent passwd | grep -vE 'nologin|false' | cut -d: -f1
    fi
}

function file_getinfo() {
    if [ -z "$2" ]; then
        echo "Error: Missing file name. Usage: internsctl file getinfo <file-name>"
        exit 1
    fi

    file="$2"

    # Check if file exists
    if [ ! -e "$file" ]; then
        echo "Error: File '$file' does not exist."
        exit 1
    fi

    if [ -z "$3" ]; then
        # No options specified, print basic file information
        stat -c "File: %n%nAccess: %A%nSize(B): %s%nOwner: %U%nModify: %y" "$file"
    else
        # Process options
        case "$3" in
            --size|-s)
                stat -c "%s" "$file"
                ;;
            --permissions|-p)
                stat -c "%A" "$file"
                ;;
            --owner|-o)
                stat -c "%U" "$file"
                ;;
            --last-modified|-m)
                stat -c "%y" "$file"
                ;;
            *)
                echo "Error: Unknown option for file. Use 'internsctl file getinfo --help' for usage information."
                exit 1
                ;;
        esac
    fi
}

# Parse command-line options
case "$1" in
    --help)
        show_help
        ;;
    --version)
        show_version
        ;;
    cpu)
        case "$2" in
            getinfo)
                get_cpu_info
                ;;
            *)
                echo "Error: Unknown option for CPU. Use 'internsctl cpu getinfo' for CPU information."
                exit 1
                ;;
        esac
        ;;
    memory)
        case "$2" in
            getinfo)
                get_memory_info
                ;;
            *)
                echo "Error: Unknown option for Memory. Use 'internsctl memory getinfo' for memory information."
                exit 1
                ;;
        esac
        ;;
    user)
        case "$2" in
            create)
                create_user "$@"
                ;;
            list)
                list_users "$@"
                ;;
            *)
                echo "Error: Unknown option for User. Use 'internsctl user --help' for usage information."
                exit 1
                ;;
        esac
        ;;
    file)
        case "$2" in
            getinfo)
                file_getinfo "$@"
                ;;
            *)
                echo "Error: Unknown option for File. Use 'internsctl file --help' for usage information."
                exit 1
                ;;
        esac
        ;;
    *)
        echo "Error: Unknown option. Use 'internsctl --help' for usage information."
        exit 1
        ;;
esac

# Rest of the script goes here, add functionality based on the requirements.