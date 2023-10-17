import re

def cleaner(input_string):
    # Remove newline characters and replace with a space
    clean_string = re.sub(r'[\n\r]+', ' ', input_string)
    
    # Remove extra white spaces (more than one space) with a single space
    clean_string = re.sub(r'\s+', ' ', clean_string).strip()
    
    return clean_string

def isDate(input_string):
    # Define a regular expression pattern to match the format
    pattern = r'\d{2}-[A-Za-z]+-\d{4}'

    # Use the re.match() function to check if the input matches the pattern
    if re.match(pattern, input_string):
        return True
    else:
        return False
    
def isDay(input_string):
    # Check if the input string ends with "day"
    if input_string.endswith("day"):
        return True
    else:
        return False
    
def class_parser(class_string, n):
    # Define a regular expression pattern to extract key-value pairs
    pattern = r'Faculty :- (.*?)\s*Course Code :- (.*?)\s*Room No\. (.*?)\s*Time :- (.*?)$'


    # Use re.search() to find the pattern in the input string
    match = re.search(pattern, class_string)

    # Initialize a dictionary to store the extracted information
    class_info = {}

    if match:
        # Extract and store the values in the dictionary
        class_info['S.No'] = n
        class_info['Faculty'] = match.group(1).strip()
        class_info['Course Code'] = match.group(2).strip()
        class_info['Room No.'] = match.group(3).strip()
        class_info['Time'] = match.group(4).strip()

        # Format the 'Time' value
        class_info['Time'] = class_info['Time'].replace('-', ' - ')

    return class_info    
