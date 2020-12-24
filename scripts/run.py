
# HOW TO RUN!
# python3 run.py -user your-user -password your-password
# At the moment no calls requrie credentials so just run:
# python3 run.py -user abc -password 123

# Default Modules
import datetime,time,os,sys

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

# To Debug: parse_args('dict',True)
my_args = parse_args('dict',False,[],['-user','-password'],False,['-password'])
if('-user' in list(my_args.keys())):
    user_from_commandline = my_args['-user'].value

if ('-password' in list(my_args.keys())):
    password_from_commandline = my_args['-password'].value

if ('-token' in list(my_args.keys())):
    token_from_commandline = my_args['-token'].value

#https://api.github.com/repos/monero-project/monero/pulls/6570
g = Github(base_url="https://api.github.com/", login_or_token=token_from_commandline)

#g = Github(login_or_token='token_bla_bla', base_url='https://github.company.com/api/v3')

###g = Github(user_from_commandline.strip(),password_from_commandline.strip())
u = g.get_user()
#print(u)

print(u)
#print(u.login)
sys.exit()
#monero-project/monero

#repo = g.get_repo("PyGithub/PyGithub")
repo_name = "monero-project/monero"
repo = g.get_repo(repo_name)

state='closed'#'open'#closed
sort='created'
base='master'
# Get open pull
pulls = repo.get_pulls(state, sort, base)
#pulls = repo.get_pull(6570)

result_type = 'unknown'
if("<class 'github.PaginatedList.PaginatedList'>" == str(type(pulls))):
    print("There are " + str(pulls.totalCount) + " " + state + " Pull Requests in " + repo_name)
    result_type = 'PaginatedList'
    #final_paginated_page = int(pulls._getLastPageUrl().split("page=")[1])
    outfile = open(OUTPUTS_DIR + state + '_' + sort + '_' + base + '_pull_requests.tab','w')
    outfile.write('Title\tPull_Request_Number\n')
    for pull in pulls:
        outfile.write(str(pull.title)+'\t'+str(pull.number)+'\n')
    outfile.close()
else:
    #print("There are " + str(len(pulls)) + " " + state + " Pull Requests in " + repo_name)
    result_type = 'list'
    print(pulls)

#if(result_type == 'PaginatedList'):
#    one_result = pulls.get_page(0)
#    print(str(pulls._getLastPageUrl().split("page=")[1]))
#    final_paginated_page = 0

#print("There are " + str(len(pulls)) + " " + state + " Pull Requests in " + repo_name)

runtime.stop()
print("Program Runtime: "+runtime.seconds_to_human_readable(runtime.get_seconds()))