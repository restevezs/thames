# File       : status_parser.py
# Author     : Rafael Estevez
# Company    : A2e technologies
# Created    : 24/09/2020
# -----------------------------------------------------------------------------
# Description: a script that summarizes all errors contained in the file 
# -------------------------------------------------------------
import subprocess
import re
import sys
from pathlib import Path
import argparse
#system imports#
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument('-l','--log',default= "", help = 'log_file')
group.add_argument('-s','--sw',action= "store_true",help = 'log_file_from_sw')
group.add_argument('-f','--fpga',action= "store_true",help = 'log_file_from_fpga')
group.add_argument('-i','--linter',action= "store_true",help = 'log_file_from_pytest')
group.add_argument('-r','--git_diff',action= "store_true",help = 'filter_run_synthesis')
args = parser.parse_args()
def main():        
    result = summarize_errors(args.log)       
    return result
class summarize_errors:
    def __init__(self,log_file):
        # take arguments 
        self.log_file = log_file
        log_path=Path(log_file)
        if not log_path.exists():
            # check the existence of files to continue the process 
            sys.exit(1)             
        self.ouput_file =  open(self.log_file)
        # open built file to use it in functions
        self.data = self.ouput_file.read()
        #read the file and assign the content to a variable
        self.ouput_file.close()
        if args.fpga:       
            self.summarize_errors_fpga()
        if args.linter:       
            self.show_errors_of_app_setup_status()          
        if args.git_diff:       
            self.filter_to_run_synthesis()
        elif args.sw:
            self.summarize_errors_sw()
        #call the methods
    def summarize_errors_fpga(self):
            '''This function is used to find and display the errors .
            '''
            x= re.compile(r'\d\d:\d\d:\d\d.\d\d\d: ERROR[^\n]*')
            #regex to used to find all the lines that contained the regex, for example, 14:07:58.841: ERROR...
            matches_fpga = x.findall(self.data)
            for match_error_fpga in matches_fpga:
               if match_error_fpga:   
                   print(match_error_fpga)
               if match_error_fpga is None:
                   return True                   
    def summarize_errors_sw(self ):
        
        '''This function is used to find and display the errors .
        '''
        y= re.compile(r".*\wrror:.*")
        #regex to used to find all the lines that contained the regex, for example, ../../Common/dmaserver/dmaserver.cpp:240:44: error:...
        matches_sw = y.findall(self.data)
        for match_error_sw in matches_sw:
            if match_error_sw:
                print(match_error_sw)                      
            if match_error_sw is None:
                return True
    def show_errors_of_app_setup_status(self):
        
            '''This function is used to filter the errors 
            information and shows in a brief resume
            '''
            x= r'((?<=\] )(.*)(?=.* at line: [0-9]+$)| Incorrect.*? :)'
            z= r"(?=\b\](.*)(?=.*$)\b)((?!\\).)*$"
            y= r'  \[.*?\]'
            matches_name = re.findall(x,self.data,re.MULTILINE)
            matches_located = re.findall(z,self.data,re.MULTILINE)
            matches_path = re.findall(y,self.data,re.MULTILINE)
            first_tuple_elements_matches_name = []
            for a_tuple in matches_name:
                first_tuple_elements_matches_name.append(a_tuple[0])
            first_tuple_elements_matches_located = []
            for atuple in matches_located:
                first_tuple_elements_matches_located.append(atuple[0])
            #The parser saves the matches in a tuple, so for utility, a new list is created.
            errors_information = [i + j for i, j in zip(first_tuple_elements_matches_located, matches_path)]
            res = []
            for i in first_tuple_elements_matches_name:
                if i not in res:
                    res.append(i)
            #This loop it's used to eliminate the repeated name tests
            matches_name = res
            for match_name in matches_name:
                print('____________',match_name,'______________')
                for i in range(len(errors_information)):
                    if i<= len(errors_information):
                        if match_name in  errors_information[i]:
                            print(errors_information[i])
                print("")
    def filter_to_run_synthesis(self):
        regex = r"(\.[^.]*$.)"
        matches_regex = re.findall(regex,self.data,re.MULTILINE | re.DOTALL | re.IGNORECASE)
        
        shortened_list= []
        converted_list = []

        for element in matches_regex:
            converted_list.append(element.strip())

        for extension in converted_list:
            if extension not in shortened_list:
                shortened_list.append(extension)
        print(shortened_list)
        if shortened_list == ['.md', '.html'] or shortened_list == ['.html','md']:
           print('no hacer nada')
        if len(shortened_list) == 1 and shortened_list == ['.md']:
           print('vamos Bien')
        if len(shortened_list) == 1 and shortened_list == ['.html']:
           print('vamos Bien')
            
if __name__ == "__main__":
      main() 
