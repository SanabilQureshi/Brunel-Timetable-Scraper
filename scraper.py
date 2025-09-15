#####################
# IMPORTS & SETUP
#####################

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import datetime
from ics import Calendar, Event

# Configure Firefox to run in headless mode
options = Options()
options.add_argument("--headless")
gecko_path = 'C:\geckodriver-v0.23.0-win64\geckodriver.exe'
driver = webdriver.Firefox(executable_path=gecko_path, options=options)

# Go to Brunel timetable page and login
driver.get('https://teaching.brunel.ac.uk/SWS-2021/login.aspx')

if 1:
    brunel_id = driver.find_element_by_xpath('//*[@id="tUserName"]').send_keys('DEMO_USERNAME')
    brunel_id_password = driver.find_element_by_xpath('//*[@id="tPassword"]').send_keys('DEMO_PASSWORD')
    login = driver.find_element_by_xpath('//*[@id="bLogin"]').click()
    My_timetable = driver.find_element_by_xpath('//*[@id="LinkBtn_mystudentsettimetable"]').click()
    Weekno = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div[3]/table/tbody/tr/td[2]/div/div[4]/table/tbody/tr/td[2]/select/option[4]').click()
    Grid_or_List = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div[3]/table/tbody/tr/td[2]/div/div[6]/table/tbody/tr/td[2]/select/option[2]').click()
    View_Timetable = driver.find_element_by_xpath('//*[@id="bGetTimetable"]').click()

#####################
### MAIN SCRAPER ####
#####################

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
typelist = ['Lec', 'Lab', 'Comp Lab', 'Prac', 'Workshop', 'Presentation', 'Meeting', 'Sem'] # types of event in the timetable

c = Calendar()
todaydate = datetime.datetime(2020, 9, 28)

# Loop through 51 weeks to scrape timetable data
for i in range(51):
    counter = 1e6
    endcheck = endcheck2 = 0
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html5lib')
    datalist = soup.find_all(['p', 'td'])
    
    # Process each timetable entry
    for item in datalist:
        itemtext = item.get_text()
        
        if endcheck == 1:
            if itemtext[0] not in ["M", "T", "W", "F"]:
                break
            else:
                endcheck = 0
                
        if endcheck2 == 1:
            if itemtext == "Activity":
                endcheck2 = 0
            else:
                break
                
        if itemtext in typelist:
            endcheck = 1
            
        if itemtext in weekdays:
            counter = -1
            todaydate += datetime.timedelta(days=1)
            if itemtext == "Monday":
                todaydate += datetime.timedelta(days=2)
            if itemtext == "Friday":
                endcheck2 = 1
                
        # Process timetable entries
        if 7 < counter < 1000:
            if counter % 8 == 0:
                calname = itemtext[0:6]
            elif counter % 8 == 1:
                calname += " " + itemtext
            elif counter % 8 == 2:
                # Start and end time parsing
                if i > 3:
                    if itemtext == "9:00":
                        calstart = str(todaydate.strftime("%Y-%m-%d 0")) + "9:00:00"
                    else:
                        timeextract = datetime.datetime.strptime(itemtext, '%H:%M')
                        # timeextract -= datetime.timedelta(hours=1)
                        timeextract = str(timeextract.strftime("%H:%M"))
                        calstart = str(todaydate.strftime("%Y-%m-%d")) + " " + timeextract + ":00"
                else:
                    if itemtext == "9:00":
                        calstart = str(todaydate.strftime("%Y-%m-%d 0")) + "8:00:00"
                    else:
                        timeextract = datetime.datetime.strptime(itemtext, '%H:%M')
                        timeextract -= datetime.timedelta(hours=1)
                        timeextract = str(timeextract.strftime("%H:%M"))
                        calstart = str(todaydate.strftime("%Y-%m-%d")) + " " + timeextract + ":00"
            elif counter % 8 == 3:
                if i > 3:
                    timeextract = datetime.datetime.strptime(itemtext, '%H:%M')
                    timeextract = str(timeextract.strftime("%H:%M"))
                    calend = str(todaydate.strftime("%Y-%m-%d")) + " " + timeextract + ":00"
                else:
                    timeextract = datetime.datetime.strptime(itemtext, '%H:%M')
                    timeextract -= datetime.timedelta(hours=1)
                    timeextract = str(timeextract.strftime("%H:%M"))
                    calend = str(todaydate.strftime("%Y-%m-%d")) + " " + timeextract + ":00"
            elif counter % 8 == 4:
                pass
            elif counter % 8 == 5:
                calloc = itemtext
            elif counter % 8 == 6:
                caldesc = itemtext
            elif counter % 8 == 7:
                # Create event in ICS file
                calname += " " + itemtext
                e = Event()
                e.name = calname
                e.begin = calstart
                e.end = calend
                e.description = caldesc
                e.location = calloc
                c.events.add(e)
                
        counter += 1
        
    next_week = driver.find_element_by_xpath('//*[@id="bNextWeek"]').click() # go to next week of timetable

with open('./My_Timetable.ics', 'w') as my_file:
    my_file.writelines(c)
    
driver.quit()

