# Default Modules
import datetime,time,os,sys,unittest

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
    """

    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1

# Get the version number for purposes of adding the right Modules folder to be imported from
python_version = sys.version
space_loc = list(find_all(python_version,' '))
python_version_clean = python_version[0:space_loc[0]].strip(' ').replace(' ','')
dot_loc = list(find_all(python_version_clean,'.'))
python_version_clean = python_version_clean[0:dot_loc[1]].strip(' ').replace(' ','').replace('.','')

# Create variables for all the paths
if((OS_TYPE == 'windows')):
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'\\'))
    OUTPUT_FILE_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\outputs\\'
    INPUT_FILE_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\inputs\\'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\scripts\\'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\modules\\python'+python_version_clean+'\\'
    CLASS_FILES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '\\classes\\'
elif((OS_TYPE == 'linux') or (OS_TYPE == 'macintosh')):
    directories = list(find_all(OUTPUT_FILE_DIRECTORY,'/'))
    OUTPUT_FILE_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/outputs/'
    INPUT_FILE_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/inputs/'
    SCRIPTS_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/scripts/'
    MODULES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/modules/python'+python_version_clean+'/'
    CLASS_FILES_DIR = OUTPUT_FILE_DIRECTORY[:directories[-1]] + '/classes/'

# OS Compatibility for importing Class Files
if((OS_TYPE == 'linux')):
    sys.path.insert(0,'../classes/')
    sys.path.insert(1,MODULES_DIR)
elif((OS_TYPE == 'windows')):
    sys.path.insert(0,'..\\classes\\')
    sys.path.insert(1,MODULES_DIR)

class ColoredText:
    """
    Custom Color Scheme
    """

    def __init__(self,color_name=[],color_code=[]):
        """
        {color_name}
            List of names you will be referencing.  This is teh name you will give each
            color to be accessed by.

        {color_code}
            List of color codes ie: 38;5;39m
            to be used in the same order as passed in by {color_name}
        """

        self.color_name_to_code = {}
        self.color_code_to_name = {}

        # Predefined colors which can be overwritten
        self.color_name_to_code['black'] = '30m'
        self.color_name_to_code['red'] = '31m'
        self.color_name_to_code['green'] = '32m'
        self.color_name_to_code['yellow'] = '33m'
        self.color_name_to_code['blue'] = '34m'
        self.color_name_to_code['purple'] = '35m'
        self.color_name_to_code['cyan'] = '36m'
        self.color_name_to_code['white'] = '37m'
        self.color_name_to_code['grey'] = '38;5;246m'
        self.color_name_to_code['orange'] = '38;5;214m'
        self.color_name_to_code['light_purple'] = '38;5;135m'
        self.color_name_to_code['dark_purple'] = '38;5;93m'
        self.color_code_to_name['30m'] = 'black'
        self.color_code_to_name['31m'] = 'red'
        self.color_code_to_name['32m'] = 'green'
        self.color_code_to_name['33m'] = 'yellow'
        self.color_code_to_name['34m'] = 'blue'
        self.color_code_to_name['35m'] = 'purple'
        self.color_code_to_name['36m'] = 'cyan'
        self.color_code_to_name['37m'] = 'white'
        self.color_code_to_name['38;5;246m'] = 'grey'
        self.color_code_to_name['38;5;214m'] = 'orange'
        self.color_code_to_name['38;5;135m'] = 'light_purple'
        self.color_code_to_name['38;5;93m'] = 'dark_purple'

        # Adding Custom Colors to the dict if they exist
        if((len(color_name) == len(color_code)) and (len(color_code) > 0)):

            counter = 0
            for name in color_name:
                self.color_name_to_code[name] = color_code[counter]
                counter += 1

            counter = 0
            for code in color_code:
                self.color_code_to_name[code] = color_name[counter]
                counter += 1
                
        # Text Affects
        self.text_affects = {}
        self.text_affects['normal'] = ''
        self.text_affects['bold'] = '1;'
        self.text_affects['disabled'] = '2;'
        self.text_affects['italic'] = '3;'
        self.text_affects['underlined'] = '4;'
        self.text_affects['reverse'] = '7;'
        self.text_affects['strike through'] = '8;'
        self.text_affects['invisible'] = '9;'
        
    def cc(self,text='',color_name='white',text_affect='normal'):
        """
        cc = Custom Colors

        Gonna be typing that alot so make it small!
        """

        # Set to True if any errors are detected
        any_errors = False
        error_message = ''

        # Build the string to be returned
        ans = "\x1b["

        # Textual Affects
        if(text_affect in list(self.text_affects.keys())):
            # Add the Affect
            ans += self.text_affects[text_affect]
        else:
            # We have an error so flag it
            any_errors = True

            # Human Readable Error Message to be printed
            error_message = 'Text Affect '
            error_message += "\x1b[" + self.text_affects['bold'] + self.color_name_to_code['red']
            error_message += text_affect + "\x1b[0m"
            error_message += ' was not an option'

        # Colors
        if(color_name in list(self.color_name_to_code.keys())):
            # Add the Color
            ans += self.color_name_to_code[color_name]
        else:
            # We have an error so flag it
            any_errors = True

            # Human Readable Error Message to be printed
            error_message = 'Text Color '
            error_message += "\x1b[" + self.text_affects['bold'] + self.color_name_to_code['red']
            error_message += color_name + "\x1b[0m"
            error_message += ' was not an option'

        # Add End or Error Message
        if(not any_errors):
            ans += text + "\x1b[0m"

        # Return the desired string or error message
        if(any_errors):
            return error_message
        else:
            return ans









