import json
import requests # Login into page, send and get requests
from bs4 import BeautifulSoup # Parse through HTMl response
import re # Required for cleaner
import pandas as pd # Create dataframe and store data

from helper import class_parser, cleaner, isDate, isDay 

login_url = ("https://academics.ncuindia.edu/Login.aspx")
loggedin_url = ("https://academics.ncuindia.edu/Student/Dashboard.aspx")
attendace = ('https://academics.ncuindia.edu/Student/AttendanceSummary.aspx')

def create_payload(username, password):
    payload = {
    '__VIEWSTATE' : '/wEPDwUKLTM5NjQ1NDY1NGRkT9poG/SrCtDH/u4qiEGtERNw2zgPFRK1T9v+dTE1qjQ=',
    '__VIEWSTATEGENERATOR' : 'C2EE9ABB',
    '__EVENTVALIDATION' : '/wEdAAjpX3DBbNjW/GrgiVdXZq4WrNW/Z105GVIxn4JwB2iJLbFFKFs+WxqZ5tK1eWiEKMzEF2wl6MsgdSfMalht9vQNGpjql+30AX+Iugw4+/2LHgxU8ynFyai4PjniekABGtp2NvjHOkq5wKoqN6Aim8WGd39wMEiroGigGt6l+80X6mxIp/STp1DiIZlnB/ujW3svIwlH1JGDDhBoUixQcMCJ',
    'rdSelect' : 'Staff',
    'txtUser' : username,
    'txtPassword' : password,
    'btnlogin' : 'Login'
    }   

    return payload

def get_attendance(username, password):
    # Create a session so that the login stays
    with requests.session() as s:

        payload = create_payload(username, password)
        
        #Logging in to the website 
        response_login = s.post(login_url, data=payload)

        #Requeting attendace page
        response_attendace = s.get(attendace)
        
        #Parsing the repsonse for the html page
        soup = BeautifulSoup(response_attendace.content, 'html.parser')
        table = soup.table

        headers = table.find_all('th')
        titles = []
        for item in headers:
            titles.append(cleaner(item.text))

        rows = table.find_all('tr')

        df = pd.DataFrame(columns=titles)

        for i in rows[1:]:
            
            # Get all td elements
            data = i.find_all('td')

            row = [cleaner(tr.text) for tr in data]
            
            # Skip the aggregate row in the webpage
            if row[1] == "Aggregate (%)":
                continue
            
            # Add data to the dataframe
            l = len(df)
            df.loc[l] = row

        return df.to_json(orient='records')



def get_timetable(username, password):
    
    # Create a session so that the login stays
    with requests.session() as s:

        payload = create_payload(username, password)

        timetable = []

        #Logging in to the website 
        response_login = s.post(login_url, data=payload)
        
        #Parsing the repsonse for the html page
        soup = BeautifulSoup(response_login.content, 'html.parser')
        
        rows = soup.find_all('tr') # Find all rows in the table
        
        flag = True # Flag to skip the table head in the loop

        # Iterate through the rows and extract data
        for row in rows:

            n = 1 # Set serial number of each class for oderly printing in app
            
            # Skippig table head
            if flag:
                flag = False
                continue


            row_dict = {'Day' : '',
                        'Date' : '',
                        'Lecture Details' : []}
            
            # Find all cells in the row
            cells = row.find_all('td')
            
            # Extract and print data from each cell
            for cell in cells:
                text = cell.text.strip()
                if(isDay(text)):
                    row_dict['Day'] = text
                elif(isDate(text)):
                    row_dict['Date'] = text
                else :
                    row_dict['Lecture Details'].append(class_parser(text, n)) 
                    n += 1

            timetable.append(row_dict)
            print(json.dumps(row_dict, indent=4))
            # Print a separator for better readability
            print("-" * 40)  # You can adjust the number of dashes as needed

        return json.dumps(timetable)




