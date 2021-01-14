# HOW TO RUN!
# python3 export_pull_requests.py -token YOURGITHUBTOKEN -output-filename try2.tab -first-pull-request 201 -final-pull-request 1000 -api-url https://api.github.com/repos/monero-project/monero/pulls/

# Default Modules
import datetime,time,os,sys,json,requests

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

#print(" Color Legend:\n")
colored_text = ColoredText(['datatype'], ['38;5;30m'])
#display = colored_text.cc(' Success', 'green')
#print(display)
#display = colored_text.cc(' Failure', 'red')
#print(display)
#display = colored_text.cc(' Number', 'blue')
#print(display)
#display = colored_text.cc(' Variable', 'purple')
#print(display)
#display = colored_text.cc(' Datatype', 'datatype')
#print(display)
#display = colored_text.cc(' Class', 'orange')
#print(display)
#print("")

# To Debug: parse_args('dict',True)
my_args = parse_args('dict',False,[],['-token','-output-filename','-first-pull-request','-final-pull-request','-api-url'],False,['-token'])#'-user' not needed?
#if('-user' in list(my_args.keys())):
#    user = my_args['-user'].value

if ('-token' in list(my_args.keys())):
    token = my_args['-token'].value

if ('-api-url' in list(my_args.keys())):
    api_url = my_args['-api-url'].value

if ('-output-filename' in list(my_args.keys())):
    output_filename = my_args['-output-filename'].value

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
    print("")
else:
    print(" Session " + colored_text.cc("Not Established", 'red') + ": " + " returned status code " + colored_text.cc(str(connection_validation.status_code), 'blue'))
    print(" [ " + colored_text.cc('Check your Token','grey') + " ] ")
    print("")
    sys.exit()

if(not (os.path.isfile(OUTPUTS_DIR+'pull_request_errors_v2.txt'))):
    os.system('touch ' + OUTPUTS_DIR+'pull_request_errors_v2.txt')

if(not (os.path.isfile(OUTPUTS_DIR+'pull_request_errors_404.txt'))):
    os.system('touch ' + OUTPUTS_DIR+'pull_request_errors_404.txt')

error_file = open(OUTPUTS_DIR+'pull_request_errors_v2.txt','a')
error_file = open(OUTPUTS_DIR+'pull_request_errors_404.txt','a')

if(not (os.path.isfile(OUTPUTS_DIR+output_filename))):
    temp_outfile = open(OUTPUTS_DIR+output_filename,'w')
    string_to_write = 'Pull_Request_Number\tTitle\tCreated_At\tUpdated_At\tClosed_At\tMerged_At\tMerged\tMerged_By\tNumber_Of_Commits\tAdditions\tDeletions\tChanged_Files\tPull_Request_State\tOriginal_Coder\t'
    string_to_write += 'Merge_Commit_SHA\tMerge_Commit_SHA_URL\tHTML_URL\tDiff_URL\tPatch_URL\tIssue_URL\tCommits_URL\n'
    temp_outfile.write(string_to_write)
    temp_outfile.close()
    del temp_outfile

outfile = open(OUTPUTS_DIR+output_filename,'a')

# Loop through pull requests
for pull_request_number in range(first_pull_request,final_pull_request+1):
    api_pull = session.get(api_url+str(pull_request_number))
    if((api_pull.status_code != 200) and (api_pull.status_code != 404)):
        message = " [ "+ colored_text.cc('Error','red')+" Status Code " + colored_text.cc(str(api_pull.status_code),'blue')
        message += " for Pull Request " + colored_text.cc(str(pull_request_number),'blue') + " ]\n"
        print(message)
        break

    if(api_pull.status_code == 404):
        print(str(pull_request_number) + "\t: Returned Status Code " + colored_text.cc("404", "blue"))
    else:
        my_data = json.loads(api_pull.text)
        string_to_write = ''

        if ('message' in my_data):
            if(my_data['message'] == "Not Found"):
                print(str(pull_request_number) + "\t: " + colored_text.cc("Not Found", "grey"))
        else:

            if ('number' in my_data):
                if (type(my_data['number']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['number']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('title' in my_data):
                if (type(my_data['title']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['title']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('created_at' in my_data):
                if (type(my_data['created_at']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['created_at']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('updated_at' in my_data):
                if (type(my_data['updated_at']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['updated_at']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('closed_at' in my_data):
                if (type(my_data['closed_at']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['closed_at']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('merged_at' in my_data):
                if (type(my_data['merged_at']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['merged_at']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('merged' in my_data):
                if (type(my_data['merged']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['merged']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('merged_by' in my_data):
                if (type(my_data['merged_by']) != type(None)):
                    if ('login' in my_data['merged_by']):
                        if (type(my_data['merged_by']['login']) == type(None)):
                            string_to_write += 'NULL\t'
                        else:
                            string_to_write += str(my_data['merged_by']['login']) + '\t'
                    else:
                        string_to_write += 'NULL\t'
                else:
                    string_to_write += 'NULL\t'
            else:
                string_to_write += 'NULL\t'

            if ('commits' in my_data):
                if (type(my_data['commits']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['commits']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('additions' in my_data):
                if (type(my_data['additions']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['additions']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('deletions' in my_data):
                if (type(my_data['deletions']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['deletions']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('changed_files' in my_data):
                if (type(my_data['changed_files']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['changed_files']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('state' in my_data):
                if (type(my_data['state']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['state']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('user' in my_data):
                if (type(my_data['user']) != type(None)):
                    if ('login' in my_data['user']):
                        if (type(my_data['user']['login']) == type(None)):
                            string_to_write += 'NULL\t'
                        else:
                            string_to_write += str(my_data['user']['login']) + '\t'
                    else:
                        string_to_write += 'NULL\t'
                else:
                    string_to_write += 'NULL\t'
            else:
                string_to_write += 'NULL\t'

            if ('merge_commit_sha' in my_data):
                if (type(my_data['merge_commit_sha']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['merge_commit_sha']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('merge_commit_sha' in my_data):
                if (type(my_data['merge_commit_sha']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += 'https://github.com/monero-project/monero/commit/' + str(my_data['merge_commit_sha']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('html_url' in my_data):
                if (type(my_data['html_url']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['html_url']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('diff_url' in my_data):
                if (type(my_data['diff_url']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['diff_url']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('patch_url' in my_data):
                if (type(my_data['patch_url']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['patch_url']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('issue_url' in my_data):
                if (type(my_data['issue_url']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['issue_url']) + '\t'
            else:
                string_to_write += 'NULL\t'

            if ('commits_url' in my_data):
                if (type(my_data['commits_url']) == type(None)):
                    string_to_write += 'NULL\t'
                else:
                    string_to_write += str(my_data['commits_url']) + '\t'
            else:
                string_to_write += 'NULL\t'

            outfile.write(string_to_write + '\n')

            print(str(pull_request_number) + "\t: " + colored_text.cc("Found", "green"))

            #error_file.write(str(pull_request_number) + '\n')
            #print(str(pull_request_number) + "\t: " + colored_text.cc("Error", "red"))

error_file.close()
outfile.close()
session.close()

runtime.stop()
print(" Program Runtime: " + runtime.human_readable_string())