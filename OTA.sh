# Run this scripit with a command 'sh ./install.sh'.
# Next just open the software using simple 'python3 update.py'.
# Make sure that you have internet connection when installing.


python3_exists() {
    # check if command exists and fail otherwise
    python3 -v "$1" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "I require $1 but it's not installed. Abort."
        exit 1
    fi
}

python3_exists
printf "Please enter 'sudo pswd'\n"
sudo apt install python3
sudo apt install python3-pip
pip3 install configparser
printf "\n"
printf "Installation process completed. You may now open the software with a command 'python3 update.py'.
printf "\n"
sleep 1 
python3 update.py


python3_exists() {
    # check if command exists and fail otherwise
    python3 -v "$1" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "I require $1 but it's not installed. Abort."
        exit 1
    fi
}

command_exists() {
    # check if command exists and fail otherwise
    command -v "$1" >/dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "I require $1 but it's not installed. Abort."
        exit 1
    fi
}