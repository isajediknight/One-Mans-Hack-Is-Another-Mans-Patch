# Default Modules
import datetime,time,os,sys,urllib3,json

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
#from github import Github
#from github import PullRequest
# < ---      End  Module Import     --- >

# Benchmark all the things
runtime = Benchmark()



#chunks = {}
#page = https.request(
#    'GET',#method =
#    'https://api.github.com/repos/monero-project/monero/pulls/7075',#url =
#    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'#headers =
    #sink = ltn12.sink.table(chunks)
#)
#local response = table.concat(chunks)
#page = https.request('GET', 'https://api.github.com/repos/monero-project/monero/pulls/7075')

#page = https.urlopen(method='GET',url='https://api.github.com/repos/monero-project/monero/pulls/7075',headers={'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})
#print(page.status)
#print(page.data)
#json.loads(x)

filename = OUTPUTS_DIR+'Monero_Pull_Request_Info.tab'
ans = input("Would you like to wipe out the existing Pull Request File? (y/n)")
if(ans=='y' or ans == 'Y'):
    outfile=open(filename,'w')
    header = 'Pull_Request_Number\tTitle\tCreated_At\tUpdated_At\tClosed_At\tMerged_At\tMerged\tMerged_By\tNumber_Of_Commits\tAdditions\tDeletions\tChanged_Files'
    header += '\tPull_Request_State\tOriginal_Coder\tMerge_Commit_SHA\tMerge_Commit_SHA_URL\tHTML_URL\tDiff_URL\tPatch_URL\tIssue_URL\tCommits_URL\n'
    outfile.write(header)
    outfile.close()
    del outfile
else:
    print("Appending to: "+filename)

outfile=open(filename,'a')
my_method = 'GET'
my_url = 'https://api.github.com/repos/monero-project/monero/pulls/'
my_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
final_pull_request_processed = 1

error_file = open(OUTPUTS_DIR+'pull_request_errors.txt','a')

# Setup the connection
https = urllib3.PoolManager()

for pull_request in range(1,7184):
    page = https.urlopen(method=my_method, url=my_url+str(pull_request), headers=my_headers)
    if(int(page.status) == 200):
        my_data = json.loads(page.data)

        string_to_write = ''

        try:
            if(type(my_data['number']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['number']) + '\t'

            if (type(my_data['title']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['title']) + '\t'

            if (type(my_data['created_at']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['created_at']) + '\t'

            if (type(my_data['updated_at']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['updated_at'])+ '\t'

            if (type(my_data['closed_at']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['closed_at']) + '\t'

            if (type(my_data['merged_at']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['merged_at']) + '\t'

            if (type(my_data['merged']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['merged']) + '\t'

            if (type(my_data['merged_by']['login']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['merged_by']['login']) + '\t'

            if (type(my_data['commits']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['commits']) + '\t'

            if (type(my_data['additions']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['additions']) + '\t'

            if (type(my_data['deletions']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['deletions']) + '\t'

            if (type(my_data['changed_files']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['changed_files']) + '\t'

            if (type(my_data['state']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['state']) + '\t'

            if (type(my_data['user']['login']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['user']['login']) + '\t'

            if (type(my_data['merge_commit_sha']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['merge_commit_sha']) + '\t'

            if (type(my_data['merge_commit_sha']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += 'https://github.com/monero-project/monero/commit/'+str(my_data['merge_commit_sha']) + '\t'

            if (type(my_data['html_url']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['html_url']) + '\t'

            if (type(my_data['diff_url']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['diff_url']) + '\t'

            if (type(my_data['patch_url']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['patch_url']) + '\t'

            if (type(my_data['issue_url']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['issue_url']) + '\t'

            if (type(my_data['commits_url']) == type(None)):
                string_to_write += '\t'
            else:
                string_to_write += str(my_data['commits_url']) + '\t'

            outfile.write(string_to_write + '\n')

            print(str(pull_request) + "\t: Found")
            final_pull_request_processed = pull_request
        except:
            error_file.write(str(pull_request)+'\n')
            print(str(pull_request) + "\t: Error")

    elif(int(page.status) == 404):
        print(str(pull_request) + "\t: Not Found")

    else:
        print(str(pull_request)+'\t: Final Pull Request Processed')
        break

    # Keep from getting banned
    time.sleep(4)

outfile.close()
error_file.close()

runtime.stop()
print("Program Runtime: "+runtime.seconds_to_human_readable(runtime.get_seconds()))