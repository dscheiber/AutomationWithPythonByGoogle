#!/usr/bin/python3

import re
import subprocess as sub
import csv
from collections import OrderedDict

#print(sub.run(["cat", "syslog.log"]))

#error_dictionary = {}
#user_dictionary = {}


def get_info(line):
    #print(line)
    #error = re.search(r"ticky: ERROR ([\w ]*) \[#[0-9]*] (\([\w]*\))", line)
    #error = re.search(r"ticky: ERROR: ([\w ]*) \[#[0-9]*] (\([\w]*\))", line)
    #line = re.search(r"[\w ]* ticky: ([\w]*) ([\w\"\' ]*)", line)a
    #working_line = re.search(r"[\w ]* ticky: ([\w]*) ([\w \'\".]*) \[#[0-9]*\] \(([\w .]*)\)", line)
    #working_line = re.search(r"[\w:]*ticky: ([\w]*) ([\w .;\'\"]*) \(([\w.]*)\)", line)
    working_line = re.search(r"[\w ]* ticky: ([\w]*) ([\w \'\".]*) \[*#*[0-9]*\]* *\(([\w .]*)\)", line)
    #print(working_line)
    log_type = working_line.group(1)
    record_desc = working_line.group(2)
    username = working_line.group(3)
    #print(log_type +" " + record_desc + " "+ username)
    return [log_type, record_desc, username]

def record_error_info(log_type, record_desc):    
    if log_type == "ERROR": #if block is logic for error type and count
        error = record_desc
        try:
            error_dictionary.update({error: error_dictionary[error]+1})
        except:
            error_dictionary.update({error: 1})
    else:
        info_add = 1

def record_user_info(log_type, username):    
    error_add = 0
    info_add = 0
    try:
        current_error = user_info_dict[username][1]
    except:
        current_error = 0
    try:
        current_info = user_info_dict[username][0]
    except:
        current_info = 0
    if log_type == "ERROR": 
        error_add = 1
    else:
        info_add = 1
    user_info_dict.update({username: [current_info + info_add, current_error + error_add]})
    #except: 
    #    user_info_dict.update({field_names[0]: username, field_names[1]: info_add, field_names[2]: error_add})
    #return user_info_dict  

def write_error_csv(error_dictionary):
    header = ['Error', 'Count']
    with open("error_message.csv", "w") as error_csv:
        writer = csv.writer(error_csv)
        writer.writerow(header)
        for entry in error_dictionary:
            print(entry)
            print (error_dictionary[entry])
            writer.writerow([entry, error_dictionary[entry]])
    error_csv.close()

def write_user_csv(user_info_list):
    header = ['Username', 'INFO', 'ERROR']
    with open("user_statistics.csv", "w") as user_csv:
        writer = csv.DictWriter(user_csv, fieldnames = header)
        writer.writeheader()
        for entry in user_info_list:
            print(entry)
            writer.writerow(entry)
    user_csv.close()

def sort_error_dict(error_dictionary):
    print(error_dictionary)
    #sorted_dictionary = dict(sorted(error_dictionary.items(), key = lambda col:col[1], reverse = True))
    value_key_pairs = ((value, key) for (key, value) in error_dictionary.items())
    sorted_value_key_pairs = sorted(value_key_pairs, reverse = True)
    print(sorted_value_key_pairs)
    sorted_dictionary = {key: value for value,key in sorted_value_key_pairs}
    #sorted_dictionary = dict(sorted_value_key_pairs)
    print(sorted_dictionary)
    return sorted_dictionary

def sort_user_dict(user_info_dict):
    #print('printing base user dict')
    #print(user_info_dict)
    sorted_dictionary = OrderedDict(sorted(user_info_dict.items()))
    #print('printing sorted user dict')
    #print(sorted_dictionary)
    return sorted_dictionary

def sort_error_dict_alt(error_dictionary):
    key_list = list(error_dictionary.keys())
    print(key_list)
    sorted_value_list = list(error_dictionary.values())
    print(sorted_value_list)
    sorted_value_list.sort(reverse = True)
    print(sorted_value_list)
    reversed_pairs = ((value, key) for (key, value) in error_dictionary.items())
    reversed_dictionary = {value : key for value,key in reversed_pairs}
    sorted_dictionary = OrderedDict()
    for value in sorted_value_list:
        print(value)
        sorted_dictionary[reversed_dictionary[value]] = value
        print(sorted_dictionary)
    print(sorted_dictionary)
    print('above is the sorted dictionary')
    print(sorted_dictionary.items())
    print('this is the ordered dict\'s items.')
    return sorted_dictionary


def main():
    global error_dictionary
    global user_info_dict
    error_dictionary = {}
    user_info_dict = {}
    user_info_list = []
    with open("syslog.log", "r") as syslog:
        for line in syslog.readlines():
            info = get_info(line)
            record_error_info(info[0], info[1])
            record_user_info(info[0], info[2])    
            #user_info_list.append(record_user_info(info[0], info[2]))
        user_info_dict = sort_user_dict(user_info_dict)
        #print("Printing sorted user info dictionary.")
        #print(user_info_dict)
        for entry in user_info_dict.keys():
            formatted_entry = {"Username": entry, "INFO": user_info_dict[entry][0], "ERROR": user_info_dict[entry][1]}
            user_info_list.append(formatted_entry)
        #print(user_info_list)
    #error_dictionary = sort_error_dict(error_dictionary)        
    error_dictionary_alt = sort_error_dict_alt(error_dictionary)
    write_error_csv(error_dictionary_alt)
    write_user_csv(user_info_list[0:8])

       # print(error_dictionary)
       # print(user_dictionary)
    syslog.close()

if __name__ == "__main__":
    main()
