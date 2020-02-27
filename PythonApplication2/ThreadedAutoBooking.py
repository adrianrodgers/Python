# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function
import mechanicalsoup
import time
from datetime import timedelta,datetime
import threading
import csv

class Login:
    def __init__(self, userName, password,br):
        br.open("https://members.brsgolf.com/theshires/login")
        loginForm = br.select_form()
        # specify username and password
        loginForm.input({"login_form[username]": userName, "login_form[password]": password})
        #submit form
        br.submit_selected()
    
    
def BookTime (playerCode,dateToBook,timeToBook,br):
    print (threading.currentThread().getName(), ' thread Starting')
    url="https://members.brsgolf.com/theshires/bookings/book/1/" + dateToBook + "/"+ timeToBook
    hh = int(timeToBook[:2])
    mm = int(timeToBook[2:])
    hhmm = datetime(1,1,1,hh,mm)
    #print(playerCode, br.get_url())  
    print (playerCode,url)
    #Booking a tee thats not open yet gives 
    #<h2 class="swal2-title" id="swal2-title" style="display: flex;">Tee time unavailable</h2>
    for i in range(5):
        br.open(url)
        print(url)
        print(br.get_url())
        #check if the url are the same if not there's a prob
        if br.get_url() == url:
            bookingForm = br.select_form()
            bookingForm.set_select({"member_booking_form[player_1]": playerCode})
            br.submit_selected()
            bookingDone = True
            break
        else:
            hhmm = hhmm + timedelta(minutes=9)
            print ("Didnt book")
            url="https://members.brsgolf.com/theshires/bookings/book/1/" + dateToBook + "/" + hhmm.strftime("%H%M")
            time.sleep(1)
                

    """
    <select id="member_booking_form_player_1" name="member_booking_form[player_1]">
    <option value="">Start typing to find player...</option>
    <option value="314">Rodgers, Adrian</option>
    </select>
    """
    #bookingForm.set_select({"member_booking_form[player_1]": playerCode})
    #br.get_current_form().print_summary()
    """
    After
    <select id="member_booking_form_player_1" name="member_booking_form[player_1]">
    <option value="">Start typing to find player...</option>
    <option selected="selected" value="314">Rodgers, Adrian</option>
    </select>
    """
    #br.submit_selected()
                                      
    
    
if __name__ == '__main__':
    print("Threaded")
    adrianSB = mechanicalsoup.StatefulBrowser()
    tonySB = mechanicalsoup.StatefulBrowser()
 
    # Get logins from c:\logins\UserDetails
    with open(r"c:\Logins\UserDetails.txt", newline='') as f:
        reader = csv.reader(f)
        y = list(reader)
    a = y[0]    #['adrian', '0326', '83468346', '314', '0921']
    t = y[1]    #['tony', '0325', 'bunkerboys18', '313', '0948']
    #
    adrianPlayerCode = a[3]
    tonyPlayerCode = t[3]
    Login(a[1],a[2],adrianSB)
    Login(t[1],t[2],tonySB)
    #
    #Add 14 days then wait till 7 am to book as the site wont be ready till then
    todaysDate = datetime.now()
    plus14days = todaysDate + timedelta(days = 14)
    dateToBook= plus14days.strftime("%Y%m%d")
    #print ("dateToBook" + dateToBook)
    
    #is it 7am yet?
    
    hh,mm,ss = todaysDate.strftime("%H,%M,%S").split(",")
    NowInSeconds = int(hh)*60*60 + int(mm)*60 + int(ss)
    waitTill = 6*60*60 + 59*60 + 59  #06:59:59
    #waitTill = NowInSeconds +2
    print (waitTill,NowInSeconds,hh,mm,ss)
    print (int(waitTill - NowInSeconds))
    if (waitTill - NowInSeconds) > 0 : 
        time.sleep( waitTill - NowInSeconds)
    print ("done waiting",datetime.now())
    
    #BookTime (tonyPlayerCode, dateToBook, "0948", tonySB)
    #BookTime (adrianPlayerCode, dateToBook, "0921", adrianSB)
    
    AdrianThread = threading.Thread(name="Adrian",target= BookTime, args=(adrianPlayerCode, dateToBook, a[4], adrianSB))
    AdrianThread.start()
    TonyThread = threading.Thread(name="Tony",target=BookTime, args=(tonyPlayerCode, dateToBook, t[4], tonySB))
    TonyThread.start()
    
    #Just a change


