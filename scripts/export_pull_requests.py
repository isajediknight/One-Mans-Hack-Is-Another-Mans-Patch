# HOW TO RUN!
# python3 export_pull_requests.py -user your-user -password your-password

# Default Modules
import datetime,time,os,sys,json

if(sys.platform.lower().startswith('linux')):
    OS_TYPE = 'linux'
elif(sys.platform.lower().startswith('mac')):
    OS_TYPE = 'macintosh'
elif(sys.platform.lower().startswith('win')):
    OS_TYPE = 'windows'
else:
    OS_TYPE = 'invalid'

# Get our current directory
OUTPUT_FILE_DIRECTORY = os.getcwd()

def find_all(a_str, sub):
    """
    Returns the indexes of {sub} where they were found in {a_str}.  The values
    returned from this function should be made into a list() before they can
    be easily used.
    Last Update: 03/01/2017
    By: LB023593
    """

    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

# Create variables for all the paths
if((OS_TYPE == 'windows')):
    # Clear Screen Windows
    os.system('cls')
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'\\'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\outputs\\'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\inputs\\'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\scripts\\'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\github\\'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\classes\\'
elif((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    # Clear Screen Linux / Mac
    os.system('clear')
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'/'))
    OUTPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/outputs/'
    INPUTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/inputs/'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/scripts/'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/'
    MODULES_GITHUB_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/github/'
    CLASSES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/classes/'

# OS Compatibility for importing Class Files
if((OS_TYPE == 'linux')):
    sys.path.insert(0,'../classes/')
    sys.path.insert(0,MODULES_DIR)
elif((OS_TYPE == 'windows')):
    sys.path.insert(0,'..\\classes\\')
    sys.path.insert(0,MODULES_DIR)

# < --- Begin Custom Classes Import --- >
# Custom Colors for printing to the screen
from custom_colors import *

# Allows Parameters to be read by Python more easily
from reuseable_methods import parse_args

from benchmark import *
# < ---  End  Custom Classes Import --- >

# < ---     Begin Module Import     --- >
from github import Github
from github import PullRequest
# < ---      End  Module Import     --- >

# Benchmark all the things
runtime = Benchmark()

print(" Color Legend:\n")
colored_text = ColoredText(['datatype'], ['38;5;30m'])
display = colored_text.cc(' Success', 'green')
print(display)
display = colored_text.cc(' Failure', 'red')
print(display)
display = colored_text.cc(' Number', 'blue')
print(display)
display = colored_text.cc(' Variable', 'purple')
print(display)
display = colored_text.cc(' Datatype', 'datatype')
print(display)
display = colored_text.cc(' Class', 'orange')
print(display)
print("")

# To Debug: parse_args('dict',True)
my_args = parse_args('dict',False,[],['-token','-first-pull-request','-final-pull-request','-api-url'],False,['-token'])#'-user' not needed?
#if('-user' in list(my_args.keys())):
#    user = my_args['-user'].value

if ('-token' in list(my_args.keys())):
    token = my_args['-token'].value

if ('-api-url' in list(my_args.keys())):
    token = my_args['-api-url'].value

if ('-first-pull-request' in list(my_args.keys())):
    try:
        first_pull_request = int(my_args['-first-pull-request'].value)
    except:
        message = " [ " + colored_text.cc('-first-pull-request','purple') + " >" + my_args['-first-pull-request'].value + "< is "+ colored_text.cc('not','red') +" an "
        message += colored_text.cc('Integer','datatype') + " ]"
        print(message)
        sys.exit()

if ('-final-pull-request' in list(my_args.keys())):
    try:
        final_pull_request = int(my_args['-final-pull-request'].value)
    except:
        message = " [ " + colored_text.cc('-final-pull-request','purple') + " >" + my_args['-final-pull-request'].value + "< is "+ colored_text.cc('not','red') +" an "
        message += colored_text.cc('Integer','datatype') + " ]"
        print(message)
        sys.exit()

# Configure the session
session = requests.Session()
session.auth=('token',token)

# Validate session can connect
connection_validation = session.get('https://api.github.com/user')
if(int(connection_validation.status_code) == 200):
    print(" Session " + colored_text.cc("Established",'green') + ": " + " returned status code " + colored_text.cc(str(connection_validation.status_code),'blue'))
else:
    print(" Session " + colored_text.cc("Not Established", 'red') + ": " + " returned status code " + colored_text.cc(str(connection_validation.status_code), 'blue'))
    print(" [ " + colored_text.cc('Check your Token','grey') + " ] ")
    sys.exit()

# Loop through pull requests
for pull_request_number in range(first_pull_request,final_pull_request+1):
    api_pull = session.get(api_url+str(pull_request_number))
    if(api_pull.status_code != 200):
        message = " [ "+ colored_text.cc('Error','red')+" Status Code " + colored_text.cc(str(api_pull.status_code),'blue')
        message += " for Pull Request " + colored_text.cc(str(pull_request_number),'blue') + "]"
        print(message)



runtime.stop()
print(" Program Runtime " + str(counter) + " Addresses in " + runtime.human_readable_string())