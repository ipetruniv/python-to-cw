import os
import sys
import glob
import datetime
from datetime import date
import re
#Values separator
separator = ' '
#Path to folder contains logs
ospath = 'c:\\logs\\*.txt'
files = glob.glob(ospath)
if not files:
    sys.exit("No files for processing")
#Debug
print(files)
#Set total amount of returned costs to 0
total_refund = 0
#Form name for new log
now = datetime.datetime.now()
#logfilename = now.strftime("%Y%m%d_%H%M") + "-cw.log"
logfilename = 'rpa-to-cloudwatch.log'
#Create the new file for import
#logfile = open (logfilename,"w")
logfile = open (logfilename,"a+")
print (logfilename)
for filename in files:
    #Paterns to search
    starttimedetect = 'Login succesfully with username'
    ticketcase_number = 'Ticketcase number '
    booking_referance = 'Booking referance - '
    totally_refunded = 'Totally refunded  - EUR'
    astute_ticket_fetch_time = 'Astute ticket fetch time: '
    astute_ticket_close_time = 'Astute ticket close time: '
    astute_total_time = 'Astute total time: '
    astral_total_time = 'Astral total time: '
    total_processing_time = 'Total processing time: '
    procesing_status = 'ERROR'
    with open(filename) as lines:
        print("Processing file: ", filename)
        #Set current ticket status as processed
        current_procesing_status = 0
        #Clear variables
        totally_refunded_summ = ''
        astute_total_time_s = ''
        astral_total_time_s = ''
        total_processing_time_s = ''
        astute_ticket_fetch_time_s = ''
        astute_ticket_close_time_s = ''
        for line in lines:
            if starttimedetect in line:
                datematch = re.search(r'\d{2}\/\d{2}\/\d{4}', line)
                date_date = datetime.datetime.strptime(datematch.group(), '%d/%m/%Y')

                timematch = re.search(r'\d{2}:\d{2}:\d{2}', line)
                date_time = datetime.datetime.strptime(timematch.group(), '%H:%M:%S')
                
                #ticketnum = line.split("number",1)[1]
                #print("Date:", date_time.date(), "The ticket number is:", ticketnum  ) 
                print ("Date:", date_date.date())
                print ("Time:", date_time.time())
                
            #Find the ticker number
            if ticketcase_number in line:
                ticket_number = (line.split(ticketcase_number,1)[1]).rstrip('\n')
                print ("Ticket number:", ticket_number)
            
            #Find the Booking referance
            if booking_referance in line:
                booked_referance = (line.split(booking_referance,1)[1]).rstrip('\n')
                print ("Booking referance:", booked_referance)

            #Find the Totally refunded summ
            if totally_refunded in line:
                totally_refunded_summ = (line.split(totally_refunded,1)[1]).rstrip('\n')
                #Astute ticket fetch time
                if totally_refunded_summ == '':
                        totally_refunded_summ = 0
                total_refund = total_refund + float(totally_refunded_summ)
                print ("Totally refunded summ:", totally_refunded_summ)
            
            #Astute fetch time
            if astute_ticket_fetch_time in line:
                astute_ticket_fetch_time_s = (line.split(astute_ticket_fetch_time,1)[1]).rstrip('\n')
                #print ("Astute total time:", astute_ticket_fetch_time_s)
            
            #Astute close time
            if astute_ticket_close_time in line:
                astute_ticket_close_time_s = (line.split(astute_ticket_close_time,1)[1]).rstrip('\n')
                #print ("Astute total time:", astute_ticket_close_time_s)
            
            #Astute total time
            if astute_total_time in line:
                astute_total_time_s = (line.split(astute_total_time,1)[1]).rstrip('\n')
                #print ("Astute total time:", astute_total_time_s)
            
            #Astral total time
            if astral_total_time in line:
                astral_total_time_s = (line.split(astral_total_time,1)[1]).rstrip('\n')
                #print ("Astral total time:", astral_total_time_s)
            
            #Total processing time
            if total_processing_time in line:
                total_processing_time_s = (line.split(total_processing_time,1)[1]).rstrip('\n')
                #print ("Total processing time:", total_processing_time_s)
            
            #Ticket status
            if procesing_status in line:
                current_procesing_status = 1
        
        #Show results
        #Astute ticket fetch time
        if astute_ticket_fetch_time_s == '':
            astute_ticket_fetch_time_s = 0
        print ("Astute ticket fetch time:", astute_ticket_fetch_time_s)
        
        #Astute ticket close time
        if astute_ticket_close_time_s == '':
            astute_ticket_close_time_s = 0
        print ("Astute ticket close time: ", astute_ticket_close_time_s)
    
        #Astute total time
        if astute_total_time_s == '':
            astute_total_time_s = 0
        print ("Astute total time:", astute_total_time_s)
        
        #Astral total time
        if astral_total_time_s == '':
            astral_total_time_s = 0
        print ("Astral total time:", astral_total_time_s)
        
        #Total processing time
        if total_processing_time_s == '':
            total_processing_time_s = 0
        print ("Total processing time:", total_processing_time_s)
        
        #Ticket status dispaly
        if current_procesing_status == 1:
            print ("Ticket procesing status is FAILED")
        else:
            print ("Ticket procesing status is OK")

        logline = date_date.strftime("%Y-%m-%d") + separator \
        + date_time.strftime("%H:%M:%S") + separator \
        + str(ticket_number) + separator \
        + str(booked_referance) + separator \
        + str(totally_refunded_summ) + separator \
        + str(astute_ticket_fetch_time_s) + separator \
        + str(astute_ticket_close_time_s)  + separator \
        + str(astute_total_time_s)  + separator \
        + str(astral_total_time_s)  + separator \
        + str(total_processing_time_s)  + separator \
        + str(current_procesing_status) + '\n'
        print ("Ready to import log line:")
        print (logline)
        logfile.write(logline)
        print ("END OF FILE \n")
    #Rename file to skip processing in the future
    file_base = os.path.splitext(filename)[0]
    os.rename(filename, file_base + '.old')

print ("Totally refund in this queue: ", total_refund)
logfile.close  

