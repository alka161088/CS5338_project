"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Assignment requirement:

Input: Each input is a *.html file, which is a downloaded webpage for a faculty member listed on
http://www.cs.txstate.edu/Personnel/Faculty Links to an external site.(e.g., http://www.cs.txstate.edu/Personnel/jg66Links to an external site.). Your program only needs to work offline locally on the downloaded input pages.

Output: Each output is a *.txt file, which contains a tabular form similar to the following, with the requested information (italic as shown below) correctly extracted from the corresponding input file.
 

Name: Ju (Byron) Gao

Education: BS, PhD, Simon Fraser University

Research interests: Data mining, databases, information retrieval

Office: CMAL 311D

Webpage: http://cs.txstate.edu/~jg66

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import html
import re

result = {}
flag = False
panel_name_dict = {'Education': 'Education', 'Research Interests': 'Research interests', 'Office Location': 'Office'}

print('Enter the html file name from which you want to extract the information')
input_file_name = input()

try:
    with open(input_file_name, 'r') as f:
        content = f.readlines()
        # Read line by line and extract required fields
        for line in content:
            # Extract Name
            if '<title>' in line:
                match = re.match(r"^.*-\s(.*)<.*$", line)
                result['Name'] = match.group(1)

            # extract Education, Research interests, and Office
            # First match the name of the field in panel title element and make flag as true
            if 'panel-title' in line:
                match = re.match(r"^.*>(.*)<.*$", line)
                panel_name = match.group(1)
                if panel_name in panel_name_dict:
                    flag = True
            # If flag is true (which means it crossed the required panel title) then it extracts information from the panel body's paragraph (<p>) element
            if flag and ('<p>' in line):
                match = re.match(r".*<p>(.*)</p><", line)
                result[panel_name_dict[panel_name]] = match.group(1)
                flag = False  

            # Extract webpage
            if '>Homepage<' in line:
                match = re.match(r'^.*=\"(.*)\".*$', line)
                result['Webpage'] = match.group(1)
        
        # Output file name, remove 'html' and add 'txt' extension in input file name, also add 'output' prefix
        output_file_name = 'output ' + input_file_name[:-4] + 'txt'
            
        file = open(output_file_name, 'w+')
        # Reorder the required fields as the result dictionary have feilds in random order
        fields_in_required_order = ['Name', 'Education', 'Research interests', 'Office', 'Webpage']
        for i in fields_in_required_order:
            # Unescape the html entities, for example - it will replace &amp; and will print only & 
            # If it does not find any field then print empty string
            file.write(i + ': ' + html.unescape(result.get(i) or '') + '\n\n')
        file.close()

except AttributeError:
    print('Error occurred, some attribute\'s information not available or could not able to extract') 
except Exception as e:
    print('Error occurred, please correct the following error: ', e ) 
