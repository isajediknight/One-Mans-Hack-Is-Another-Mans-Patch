def parse_args(return_type='dict',print_debug=False,insert_values=[],required=[],reset_argv=False,hide_user_entries=[]):
    """
        Variables
            return_type (string)
                dict
                    dictionary of namedtuples
                list
                    list of namedtuples
            print_debug (boolean)
                Will print various debugging statements
            insert_values
                list containing additional parameters/values to be inserted into argv
                it will appear as if these were added to the end of commandline parameters
            required
                list of parameters required
                if any of these are missing it will prompt for them
            reset_argv
                if True it will pop all items in argv except for argv[0] (the script file name called)
            hide_user_entries
                any parameters in this list if they are also in required and not sent in as parameters
                will be gotten from the user hiding the text from the screen as it is typed
        Open Items
        1)  Linux compatibility has not been added
        2)  
        Assumptions
        1)  insertion_order will always be the last insert for a value
            this only matters if a parameter was overwritten
        2)  only tested on Python 3.4.3
    """

    import sys, os, getpass
    from collections import namedtuple

    printed_yet = False
    for item in hide_user_entries:
        if(item not in required):
            if(not printed_yet):
                print("[ Parameters Missing from 'required' but are in 'hide_user_entries']\n")
                printed_yet = True
            print(item)

    if(printed_yet):
        print("")

    # Pop all values from argv except the python filename
    printed_yet = False
    fix_pop_order = []
    if(reset_argv):
        if(print_debug and (len(sys.argv) > 1)):
            print("[ Popping values from argv ]\n")
            printed_yet = True
        while(len(sys.argv) > 1):
            fix_pop_order.append(sys.argv.pop())
        if(print_debug and printed_yet):
            counter = 1
            for item in reversed(fix_pop_order):
                print(" " + str(counter) + " : " + item)
                counter += 1
            print("")
    
    # Add items to the commandline variable
    if(len(insert_values) > 0):
        for insert in insert_values:
            sys.argv.append(insert)

    # If a required parameter is missing get it
    # !!!This does not validate the user entries!!!
    printed_yet = False
    for required_parameters in required:
        if(required_parameters not in sys.argv):
            if(not printed_yet):
                print("[ Some required parameters are missing - prompting now ]\n")
                printed_yet = True
            sys.argv.append(required_parameters)
            if(required_parameters in hide_user_entries):
                sys.argv.append(getpass.getpass(required_parameters + ": "))
            else:
                sys.argv.append(input(required_parameters + ": "))

    # Spacing for debugging
    if(printed_yet or print_debug):
        print("")

    # Values to return
    values = 'parameter value value_overwritten file directory relative absolute parameter_index value_index insertion_order_history'
    nt = namedtuple('parameters',values)

    # Return variable for the method
    ans = {}

    # Random characters to split the string by
    unique_splitter = "<`*~>"

    # Count the number of attempts to get a unique splitter
    counter = 0
    # Is the splitter unique? - setting to True to enter the loop
    not_unique = True
    while(not_unique):
        # Reset for each attempt
        not_unique = False
        for argument in sys.argv:
            if(unique_splitter in argument):
                # Splitter is not unique
                # Add ! to the end and try again
                unique_splitter += "!"
                not_unique = True
                counter += 1
                break

    # Display attempts to get a unique splitter
    if(print_debug):
        print("[ Attempts to get unique splitter: " + str(counter) + " ]")

    max_number_string_length = len(str(len(sys.argv)))

    if(print_debug):
        print("\n[ Parameters Passed In ]")
    counter = 0
    huge_string_v1 = ""
    huge_string_v2 = ""
    for index in range(0,len(sys.argv)):
        if(index < 10):
            if(print_debug):
                print(" " + str(index).ljust(max_number_string_length+1," ") + ": " + sys.argv[index])
        else:
            if(print_debug):
                print(" " + str(index).ljust(max_number_string_length+1," ") + ": " + sys.argv[index])
        huge_string_v1 += sys.argv[index] + " "
        huge_string_v2 += sys.argv[index] + unique_splitter
        counter += 1

    # Two options for splitting the commandline values
    huge_string_v1 = huge_string_v1[0:-1]
    huge_string_v2 = huge_string_v2[0:-len(unique_splitter)]

    # Two different ways of splitting the parameter
    list_v1 = huge_string_v1.split(" ")
    list_v2 = huge_string_v2.split(unique_splitter)

    # Count the number of parameters passed in
    PARAMETER_COUNT = len(list_v2)

    if(print_debug):
        # <--- Begin Debugging --->
        print("\n[ String ]")
        print(huge_string_v1)
        print("\n[ List v1 ]")
        print(list_v1)
        print("\n[ List v2 ]")
        print(list_v2)
        print("")
        if(list_v1 != list_v2):
            print("[ Double Quotes resulted in a different Split ]")
        else:
            print("[ v1 and v2 splits matched ]")
        # <---  End  Debugging --->

    # Triggered means that a '-' was passed in and we need to save the next value to that parameter
    triggered = False
    # Count the number of values saved to parameters
    triggered_counter = 0

    # Used to figure out how to print spaces better for parameters and values
    max_parameter_length_not_value = 0
    max_parameter_length_value = 0

    # Tracks the input location / index we are on
    index_counter = 0

    # Loop through the list with all best parsed parameters to get the max lengths
    for item in list_v2:
        if((item[0] == '-') and (len(item) > max_parameter_length_not_value)):
            max_parameter_length_not_value = len(item)
        else:
            triggered = True
            triggered_counter += 1

        if((item[0] == '-') and (index_counter == PARAMETER_COUNT-1)):
            pass
        elif((item[0] == '-') and (index_counter < PARAMETER_COUNT) and (max_parameter_length_value < len(list_v2[index_counter+1]))):
            max_parameter_length_value = len(list_v2[index_counter+1])
        elif((item[0] != '-') and (max_parameter_length_value < len(list_v2[index_counter]))):
            max_parameter_length_value = len(list_v2[index_counter])

        if((index_counter == PARAMETER_COUNT-1) and (item[0] == '-') and (max_parameter_length_value < len("< None >"))):
            max_parameter_length_value = len("< None >")
            
        index_counter += 1

    # If there were values without parameters
    if(triggered and (max_parameter_length_not_value < len("-unassigned_" + str(triggered_counter)))):
        max_parameter_length_not_value = len("-unassigned_" + str(triggered_counter))

    #if(max_parameter_length_not_value < 15):
    #    max_parameter_length_not_value = 20

    # used to count which index of the parameters we are on
    counter = 0

    # parameters and their corresponding values saved
    parameter_dict = {}

    # indexes we have saved
    # also used to check which are not saved later
    # so we can assign unsaved status to them and save them
    assigned_indexes = []

    # Variables for saving the order of values saved
    key_insertion_order_parameter = []
    key_insertion_order_value = []
    key_insertion_order_index = []
    counter_to_parameter = []
    counter_to_value = []

    # Set to True if any value of a parameter is overwritten
    overwrite_flag = False

    if(print_debug):
        # Debugging
        print("\n[ Assigning Values ]\n")
        print(" " + "Indexes".ljust(12-len("Indexes")," ") + " | Parameter".ljust(max_parameter_length_not_value+3," ") + " | " + "Value".ljust(max_parameter_length_value," ") + " | Details")

    # Which item in list_v2 are we on?
    counter = 0

    # Counts the number of unassigned values
    unassigned_counter = 0

    for item in list_v2:

        # Placeholder variables used to build namedtuple containing all data
        # passed in to the program by the user
        this_parameter = None
        this_value = None

        # If the current item is a parameter and we are not at the end of the parameters
        if(item[0] == '-' and (counter+1 < PARAMETER_COUNT)):
            if((counter+1) not in assigned_indexes):
                assigned_indexes.append(counter+1)
                ##print(item + " " + str(counter+1) + " Removed " + list_v2[counter])
            if((counter+2) not in assigned_indexes):
                assigned_indexes.append(counter+2)
                ##print(item + " " + str(counter+2) + " Removed " + list_v2[counter+1])

            # Brute Force logic works while counter is less than 100
            what_to_subtract = -1
            if(counter > 9 and counter+1 > 9):
                what_to_subtract += 2
            elif(counter < 9 and counter+1 > 9):
                what_to_subtract += 1
            else:
                what_to_subtract = 1

            if(item in parameter_dict.keys()):
                # Records duplicate parameters were used
                overwrite_flag = True

                # Make uses of these easier to follow
                this_parameter = item
                this_value = list_v2[counter+1]
                
                # Tracks the values which were replaced
                replaced_value = parameter_dict[this_parameter]
                parameter_dict[this_parameter] = this_value

                # <--- Begin File / Dir analysis --->
                if(this_value == None):
                    this_value = " < None > "

                # Initialize Checks
                dir_check = False
                relative_path = False

                # See if it is a relative file path
                file_check = os.path.isfile(this_value)

                # See if it is an absolute file path
                if(os.path.isfile(os.getcwd() + '\\' + this_value)):
                    file_check = True
                elif(file_check):
                    relative_path = True

                # Is it a relative or an absolute directory
                if(os.path.isdir(os.getcwd() + '\\' + this_value)):
                    dir_check = True
                elif(os.path.isdir(this_value)):
                    dir_check = True
                    relative_path = True

                # Human readable text output
                if(file_check and not relative_path):
                    value_type = "Relative Path to File"
                elif(file_check and relative_path):
                    value_type = "Abosulte Path to File"
                elif(dir_check and not relative_path):
                    value_type = "Relative Path to Directory"
                elif(dir_check and relative_path):
                    value_type = "Absolute Path to Directory"
                else:
                    value_type = "Neither"

                ans[this_parameter] = nt(this_parameter, parameter_dict[this_parameter], False, file_check, dir_check, relative_path, not relative_path, counter+1, counter+2, [(counter+1,counter+2)])
                # <---  End  File / Dir analysis --->

                # Index
                print_this = " " + (str(counter) + "," + str(counter+1)).ljust(8-what_to_subtract," ")
                # Parameter
                print_this += " | " + this_parameter.ljust(max_parameter_length_not_value," ")
                # Value
                print_this += " | " + this_value + " ".ljust(max_parameter_length_value-len(this_value)," ")
                # Details
                print_this += "| Previous Value: " + replaced_value + " "
                # Type
                print_this += "| " + value_type

                if(print_debug):
                    print(print_this + "#1")
            else:
                # Save this Parameter/Value pair as a more human readable variable name
                this_parameter = item
                this_value = list_v2[counter+1]
                
                parameter_dict[this_parameter] = this_value

                # <--- Begin File / Dir analysis --->
                if(this_value == None):
                    this_value = " < None > "

                # Initialize Checks
                dir_check = False
                relative_path = False

                # See if it is a relative file path
                file_check = os.path.isfile(this_value)

                # See if it is an absolute file path
                if(os.path.isfile(os.getcwd() + '\\' + this_value)):
                    file_check = True
                elif(file_check):
                    relative_path = True

                # Is it a relative or an absolute directory
                if(os.path.isdir(os.getcwd() + '\\' + this_value)):
                    dir_check = True
                elif(os.path.isdir(this_value)):
                    dir_check = True
                    relative_path = True

                # Human readable text output
                if(file_check and not relative_path):
                    value_type = "Relative Path to File"
                elif(file_check and relative_path):
                    value_type = "Abosulte Path to File"
                elif(dir_check and not relative_path):
                    value_type = "Relative Path to Directory"
                elif(dir_check and relative_path):
                    value_type = "Absolute Path to Directory"
                else:
                    value_type = "Neither"

                ans[this_parameter] = nt(this_parameter, parameter_dict[this_parameter], False, file_check, dir_check, relative_path, not relative_path, counter, counter+1, [(counter,counter+1)])
                # <---  End  File / Dir analysis --->

                # Index
                print_this = " " + (str(counter) + "," + str(counter+1)).ljust(8-what_to_subtract," ")
                # Parameter
                print_this += " | " + this_parameter.ljust(max_parameter_length_not_value," ")
                # Value
                # Yeah so +1 here is because I am lazy
                print_this += " | " + this_value + " ".ljust(max_parameter_length_value-len(this_value)+1," ")
                # Details
                print_this += "|"
                # Type
                print_this += "| " + value_type

                if(print_debug):
                    print(print_this + "#2")

            # Tracking order in which values weresaved
            #print(" " + item.ljust(max_parameter_length_not_value," ") + " : " + list_v2[counter+1])
            key_insertion_order_parameter.append(item)
            key_insertion_order_value.append(list_v2[counter+1])
            key_insertion_order_index.append(counter+1)
            counter_to_value.append(list_v2[counter+1])
            counter_to_parameter.append(item)

        # If the current item is a parameter ... and we're at the end?
        elif(item[0] == '-'):

            previously_assigned_flag = False
            if(item in parameter_dict.keys()):
                # Records duplicate parameter was used
                overwrite_flag = True
                
                # Tracks the values which were replaced
                replaced_value = parameter_dict[item]
                parameter_dict[item] = None
                previously_assigned_flag = True

                # Save this Parameter/Value pair
                this_parameter = item
                this_value = None

            # Save this Parameter/Value pair in a more human readable way
            this_parameter = item
            this_value = None
            
            parameter_dict[this_parameter] = None

            # <--- Begin File / Dir analysis --->
            if(this_value == None):
                this_value = " < None > "

            # Initialize Checks
            dir_check = False
            relative_path = False

            # See if it is a relative file path
            file_check = os.path.isfile(this_value)

            # See if it is an absolute file path
            if(os.path.isfile(os.getcwd() + '\\' + this_value)):
                file_check = True
            elif(file_check):
                relative_path = True

            # Is it a relative or an absolute directory
            if(os.path.isdir(os.getcwd() + '\\' + this_value)):
                dir_check = True
            elif(os.path.isdir(this_value)):
                dir_check = True
                relative_path = True

            # Human readable text output
            if(file_check and not relative_path):
                value_type = "Relative Path to File"
            elif(file_check and relative_path):
                value_type = "Abosulte Path to File"
            elif(dir_check and not relative_path):
                value_type = "Relative Path to Directory"
            elif(dir_check and relative_path):
                value_type = "Absolute Path to Directory"
            else:
                value_type = "Neither"
            # <---  End  File / Dir analysis --->
        
            if((counter+1) not in assigned_indexes):
                assigned_indexes.append(counter+1)

            # Brute Force logic works while counter is less than 100
            what_to_subtract = -1
            if(counter > 9):
                what_to_subtract += 0
            elif(counter <= 9):
                what_to_subtract = -1
            else:
                what_to_subtract = 0

            if(previously_assigned_flag):
                # Reassigns values if this parameter already exists
                ans[this_parameter] = ans[this_parameter]._replace(parameter = this_parameter)
                ans[this_parameter] = ans[this_parameter]._replace(value = this_parameter)
                ans[this_parameter] = ans[this_parameter]._replace(value_overwritten = True)
                ans[this_parameter] = ans[this_parameter]._replace(file = file_check)
                ans[this_parameter] = ans[this_parameter]._replace(directory = dir_check)
                ans[this_parameter] = ans[this_parameter]._replace(relative = relative_path)
                ans[this_parameter] = ans[this_parameter]._replace(absolute = not relative_path)
                ans[this_parameter] = ans[this_parameter]._replace(insertion_order_history = ans[this_parameter].insertion_order_history + (counter,counter+1))
                ans[this_parameter] = ans[this_parameter]._replace(parameter_index = counter)
                ans[this_parameter] = ans[this_parameter]._replace(value_index = counter + 1)

                # Example from other repo
                #CONSTANTS = CONSTANTS._replace(PLATFORM = 'windows')
                
                # Index
                print_this = " " + str(counter).ljust(6-what_to_subtract," ")
                # Parameter
                print_this += " | " + this_parameter.ljust(max_parameter_length_not_value," ")
                # Value
                print_this += " | < None > "
                # Details
                print_this += "| Previous Value: " + replaced_value + " "
                # Type
                print_this += "| " + value_type

                if(print_debug):
                    print(print_this + "#4")
            else:
                ans[this_parameter] = nt(this_parameter, parameter_dict[this_parameter], False, file_check, dir_check, relative_path, not relative_path, counter+1, -1, [(counter+1,-1)])
                
                # Index
                print_this = " " + str(counter).ljust(6-what_to_subtract," ")
                # Parameter
                print_this += " | " + this_parameter.ljust(max_parameter_length_not_value," ")
                # Value
                print_this += " | < None > "
                # Details
                print_this += " | "
                # Type
                print_this += "| Neither"

                if(print_debug):
                    print(print_this + "#5")

            # Tracking order in which values were saved
            key_insertion_order_parameter.append(this_parameter)
            key_insertion_order_value.append(None)
            key_insertion_order_index.append(counter+1)
            counter_to_value.append(None)
            counter_to_parameter.append(this_parameter)

        # If we are dealing with a value without a parameter
        elif((counter+1) not in assigned_indexes):

            # Used to track the values without parameters
            sub_counter = 0

            # Gets a unique '-unassigned_#' that has not been used
            while("-unassigned_" + str(unassigned_counter+sub_counter) in parameter_dict):
                sub_counter += 1

            # Makes it work for any counter less than 100
            # I've not tested it for over 100 and I don't plan on to
            if(counter > 9):
                what_to_subtract = len(str(counter))-1
            else:
                what_to_subtract = len(str(counter))

            # Save this Parameter/Value pair
            this_parameter = "-unassigned_" + str(unassigned_counter+sub_counter)
            this_value = item

            parameter_dict[this_parameter] = this_value

            # <--- Begin File / Dir analysis --->
            if(this_value == None):
                this_value = " < None > "

            # Initialize Checks
            dir_check = False
            relative_path = False

            # See if it is a relative file path
            file_check = os.path.isfile(this_value)

            # See if it is an absolute file path
            if(os.path.isfile(os.getcwd() + '\\' + this_value)):
                file_check = True
            elif(file_check):
                relative_path = True

            # Is it a relative or an absolute directory
            if(os.path.isdir(os.getcwd() + '\\' + this_value)):
                dir_check = True
            elif(os.path.isdir(this_value)):
                dir_check = True
                relative_path = True

            # Human readable text output
            if(file_check and not relative_path):
                value_type = "Relative Path to File"
            elif(file_check and relative_path):
                value_type = "Abosulte Path to File"
            elif(dir_check and not relative_path):
                value_type = "Relative Path to Directory"
            elif(dir_check and relative_path):
                value_type = "Absolute Path to Directory"
            else:
                value_type = "Neither"

            ans[this_parameter] = nt(this_parameter, parameter_dict[this_parameter], False, file_check, dir_check, relative_path, not relative_path, counter, counter+1, [(counter,counter+1)])
            # <---  End  File / Dir analysis --->

            # Index
            print_this = " " + (str(counter)).ljust(9-what_to_subtract," ")
            # Parameter
            print_this += "| " + this_parameter.ljust(max_parameter_length_not_value-len(this_parameter)," ")
            # Value
            print_this += " | " + this_value.ljust(max_parameter_length_value+1," ")
            # Details
            print_this += "|"
            # Type
            print_this += "| " + value_type

            if(print_debug):
                print(print_this + "#6")

            # Tracking order in which values were saved
            key_insertion_order_parameter.append("-unassigned_" + str(unassigned_counter+sub_counter))
            key_insertion_order_value.append(item)
            key_insertion_order_index.append(counter+1)
            counter_to_value.append(item)
            counter_to_parameter.append("-unassigned_" + str(unassigned_counter+sub_counter))

            # Counts the number of values without a parameter
            unassigned_counter += 1

        else:
            if(counter not in assigned_indexes):
                print("!!! Index " + str(counter) + " was not correctly recorded !!!")

        # Increment item counter of list_v2 items
        counter += 1

    if(print_debug):
        # Were any values of a Parameter overwritten?
        if(overwrite_flag):
            print("\n[ Values of Parameter(s) were overwritten ]")
        else:
            print("\n[ All Parameters are unique ]")

    # Used for identifying which values have no parameter
    all_parameter_indexes = list(range(1,PARAMETER_COUNT+1))
    unused_indexes = list(set(all_parameter_indexes) - set(assigned_indexes))

    # Convert the dictionary to a list
    if(return_type == 'list'):
        ans_list = []

        # Used to get the list order right
        dict_keys_for_list_order_insertion = []

        # Loop through the dictionary and insert the data so the parameters are in order
        while(len(dict_keys_for_list_order_insertion) < len(ans)):
            # Arbitrary number that is high
            smallest_index = 1000
            # The key associated with the smallest index not yet added
            smallest_key = ''
            for key in ans.keys():
                if((ans[key].parameter_index < smallest_index) and (key not in dict_keys_for_list_order_insertion)):
                    smallest_index = ans[key].parameter_index
                    smallest_key = key
            dict_keys_for_list_order_insertion.append(smallest_key)
            ans_list.append(ans[smallest_key])

        # Parameters in list form
        return ans_list
    else:
        # Parameters in dictionary form
        return ans