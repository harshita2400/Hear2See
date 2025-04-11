
from django.shortcuts import render, redirect
from . import forms
from . import models
from .models import Details
from .models import Compose
import imaplib,email
import speech_recognition as sr
from gtts import gTTS
import os
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import JsonResponse
import re
from django.conf import settings

import asyncio
import edge_tts

file = "good"
i="0"
passwrd = ""
addr = ""
item =""
subject = ""
body = ""
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = os.path.join(settings.BASE_DIR, "homepage", "attachments")

# def texttospeech(text, filename):
#     filename = filename + '.mp3'
#     flag = True
#     while flag:
#         try:
#             tts = gTTS(text=text, lang='en', slow=False)
#             tts.save(filename)
#             flag = False
#         except:
#             print('Trying again')
#     playsound(filename)
#     os.remove(filename)
#     return


async def edge_text_to_speech(text, filename="output.mp3"):
    communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await communicate.save(filename)
    playsound(filename)
    os.remove(filename)

def smooth_text(text):
    # Be careful: only do this where it doesn't ruin meaning
    text = text.replace('. ', ', ')
    return text

# To call from a sync function:
def texttospeech(text, filename="voice"):
    text = smooth_text(text)
    asyncio.run(edge_text_to_speech(text, filename + ".mp3"))

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp



def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        text1 = "Welcome to Hear to see, your very own Voice based Email service. Login with your email account in order to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            # addr = addr.replace(' ', '')
            # addr = addr.replace('attherate', '@')
            if addr != 'N':
                texttospeech("You meant " + addr + " say proceed to confirm or retry to enter again ", file + i)
                i = i + str(1)
                # say="correct"
                say = speechtotext(5)
                print(say)
                say=say.replace(' ','')
                # flag = False
                # if say == 'yes' or say == 'Yes':
                if("retry" in say.lower() or say == 'N'):
                    print(say.lower())
                    print("User confirmation captured as:", addr)
                    flag = True
                elif("proceed" in say.lower()):
                    flag=False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        request.email = addr

        flag = True
        while (flag):
            texttospeech("Enter your password", file + i)
            i = i + str(1)
            passwrd = speechtotext(12)
            
            if addr != 'N':
                texttospeech("You meant " + passwrd + " say proceed to confirm or retry to enter again", file + i)
                i = i + str(1)
                # say="correct"
                # flag = False
                say = speechtotext(3)
                print(say)
                say = say.replace(" ", "")
                if('retry' in say.lower() or say == 'N'):
                    say = speechtotext(3)
                    print("User confirmation captured as:", say)
                    flag = True
                elif('proceed' in say.lower()):
                    flag = False
                
                     
                
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)

        imap_url = 'imap.gmail.com'
        passwrd = 'fzsyyzmskthalsvn'
        addr = 'hackmol600@gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, passwrd)
            s.login(addr, passwrd)
            texttospeech("You have logged in successfully.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

    
    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 

def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. How would you like to proceed ?", file + i)
        i = i + str(1)
        # while(flag):
        texttospeech("To compose an email say compose. To open Inbox folder say Inbox. To Logout say Logout.", file + i)
        i = i + str(1)
            # say=""
            # say = speechtotext(3)
            # print(say)
            # if 'no' in say.lower():
            #     flag = False
        texttospeech("Enter your desired action", file + i)
        i = i + str(1)
        act = speechtotext(5)
        act = act.lower()
        act= act.replace(' ','')
        if act == 'compose':
            return JsonResponse({'result' : 'compose'})
        elif act == 'inbox':
            return JsonResponse({'result' : 'inbox'})
        elif act == 'sent':
            return JsonResponse({'result' : 'sent'})
        elif act == 'trash':
            return JsonResponse({'result' : 'trash'})
        elif 'logout' in act:
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",file + i)
            i = i + str(1)
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'homepage/options.html')

def compose_view(request):
    global i, addr, passwrd, s, item, subject, body
    if request.method == 'POST':
        text1 = "You have reached the page where you can compose and send an email. "
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        flag1 = True
        fromaddr = addr
        toaddr = list()
        while flag1:
            while flag:
                texttospeech("enter receiver's email address:", file + i)
                i = i + str(1)
                to = ""
                to = speechtotext(15)
                if to != 'N':
                    
                    texttospeech("You meant " + to + " say proceed to confirm or retry to enter again", file + i)
                    i = i + str(1)
                    # say="confirm"
                    # flag = False
                    toaddr.append(to)
                    say = speechtotext(5)
                    if "retry" in say.lower():
                        toaddr.remove(to)
                        flag = True
                    elif("proceed" in say.lower()):
                        flag=False
                else:
                    texttospeech("could not understand what you meant", file + i)
                    i = i + str(1)
            texttospeech("Do you want to enter more recipients ?  if yes say add else say proceed.", file + i)
            i = i + str(1)
            say1 = speechtotext(5)
            say1 = say1.replace(" ","")
            if "proceed" in say1.lower():
                flag1 = False
            elif "add" in say1.lower():
                flag1 = True
            flag = True

        newtoaddr = list()
        for item in toaddr:
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
            newtoaddr.append(item)
            print(item)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(newtoaddr)
        flag = True
        while (flag):
            texttospeech("enter subject", file + i)
            i = i + str(1)
            subject = speechtotext(20)
            if subject == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            texttospeech("enter body of the mail", file + i)
            i = i + str(1)
            body = speechtotext(30)
            if body == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False

        msg.attach(MIMEText(body, 'plain'))
        texttospeech("any attachment? say attach to include or skip to continue", file + i)
        i = i + str(1)
        x = speechtotext(5)
        x = x.lower()
        x = x.replace(" ","")
        if 'skip' in x:
            print(x)
        else:
            texttospeech("Do you want to record an audio or send an attachment? say audio or attachment", file + i)
            i = i + str(1)
            say = speechtotext(2)
            say = say.lower()
            say = say.replace(" ","")
            print(say)
            if 'attachment' in say:
                texttospeech("Enter filename with extension", file + i)
                i = i + str(1)
                # filename = speechtotext(5)
                filename = "photo.png"
                filename = filename.strip()
                filename = filename.replace(' ', '')
                filename = filename.lower()
                filename = convert_special_char(filename)
                
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)

                
            elif 'audio' in say:
                texttospeech("Enter filename.", file + i)
                i = i + str(1)
                filename = speechtotext(5)
                filename = filename.lower()
                filename = filename + '.mp3'
                filename = filename.replace(' ', '')
                print(filename)
                texttospeech("Enter your audio message.", file + i)
                i = i + str(1)
                audio_msg = speechtotext(20)
                flagconf = True
                while flagconf:
                    try:
                        tts = gTTS(text=audio_msg, lang='en', slow=False)
                        tts.save(filename)
                        flagconf = False
                    except:
                        print('Trying again')
                attachment = open(filename, "rb")
                p = MIMEBase('application', 'octet-stream')
                p.set_payload((attachment).read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(p)
           
                
        try:
            s.sendmail(fromaddr, newtoaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
        except Exception as e:
            print("An error occurred:", e)
            
            texttospeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        s.quit()
        return JsonResponse({'result' : 'success'})
    
    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body

    return render(request, 'homepage/compose.html', {'compose' : compose})
   
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def get_attachment(msg):
    global i
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                texttospeech("Attachment has been downloaded", file + i)
                i = i + str(1)
                path = 'C:/Users/Chacko/Desktop/'
                files = os.listdir(path)
                paths = [os.path.join(path, basename) for basename in files]
                file_name = max(paths, key=os.path.getctime)
            with open(file_name, "rb") as f:
                if file_name.find('.jpg') != -1:
                    texttospeech("attachment is an image", file + i)
                    i = i + str(1)
                if file_name.find('.png') != -1:
                    texttospeech("attachment is an image", file + i)
                    i = i + str(1)
                if file_name.find('.mp3') != -1:
                    texttospeech("Playing the downloaded audio file.", file + i)
                    i = i + str(1)
                    playsound(file_name)


def read_mails(mail_list,folder):
    global s, i
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        result, email_data = conn.fetch(item, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        texttospeech("Email number " + str(mail_count + 1) + "    .The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject, file + i)
        i = i + str(1)
        print('message id= ', Msg_id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")
        to_read_list.append(Msg_id)
        mail_count = mail_count + 1

    flag = True
    while flag :
        n = 0
        flag1 = True
        # while flag1:
        #     texttospeech("Enter the email number of mail you want to read.",file + i)
        #     i = i + str(1)
        #     n = speechtotext(5)
        #     print(n)
        #     texttospeech("You meant " + str(n) + ". Say yes or no.", file + i)
        #     i = i + str(1)
        #     say = speechtotext(2)
        #     say = say.lower()
        #     if say == 'yes':
        #         flag1 = False
        n = int(n)
        msgid = to_read_list[n - 1]
        print("message id is =", msgid)
        typ, data = conn.search(None, '(HEADER Message-ID "%s")' % msgid)
        data = data[0]
        result, email_data = conn.fetch(data, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        texttospeech("The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject, file + i)
        i = i + str(1)
        Body = get_body(message)
        Body = Body.decode()
        Body = re.sub('<.*?>', '', Body)
        Body = os.linesep.join([s for s in Body.splitlines() if s])
        if Body != '':
            texttospeech(Body, file + i)
            i = i + str(1)
        else:
            texttospeech("Body is empty.", file + i)
            i = i + str(1)
        get_attachment(message)


        texttospeech("Email ends here.", file + i)
        i = i + str(1)
        texttospeech("Do you want to read more mails?", file + i)
        i = i + str(1)
        ans = speechtotext(2)
        ans = ans.lower()
        if ans == "no":
            flag = False

def search_specific_mail(folder,key,value,foldername):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None,key,'"{}"'.format(value))
    mail_list=data[0].split()
    if len(mail_list) != 0:
        texttospeech("There are " + str(len(mail_list)) + " emails with this email ID.", file + i)
        i = i + str(1)
    if len(mail_list) == 0:
        texttospeech("There are no emails with this email ID.", file + i)
        i = i + str(1)
    else:
        read_mails(mail_list,foldername)

def inbox_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, passwrd)
        conn.select('"INBOX"')
        result, data = conn.search(None, '(UNSEEN)')
        unread_list = data[0].split()
        no = len(unread_list)
        result1, data1 = conn.search(None, "ALL")
        mail_list = data1[0].split()
        text = "You have reached your inbox. There are " + str(len(mail_list)) + " total mails in your inbox. You have " + str(no) + " unread emails" + ". To read unread emails say unread. To search a specific email say search. To go back to the menu page say back. To logout say logout."
        texttospeech(text, file + i)
        i = i + str(1)
        flag = True
        while(flag):
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'unread':
                flag = False
                if no!=0:
                    read_mails(unread_list,'inbox')
                else:
                    texttospeech("You have no unread emails.", file + i)
                    i = i + str(1)
            elif act == 'search':
                flag = False
                emailid = ""
                while True:
                    texttospeech("Enter email ID of the person who's email you want to search.", file + i)
                    i = i + str(1)
                    emailid = speechtotext(15)
                    texttospeech("You meant " + emailid + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    yn = speechtotext(5)
                    yn = yn.lower()
                    if not('no' in yn):
                        break
                emailid = emailid.strip()
                emailid = emailid.replace(' ', '')
                emailid = emailid.lower()
                emailid = convert_special_char(emailid)
                search_specific_mail('INBOX', 'FROM', emailid,'inbox')

            elif act == 'back':
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            elif act == 'log out':
                addr = ""
                passwrd = ""
                texttospeech("You have been logged out of your account and now will be redirected back to the login page.", file + i)
                i = i + str(1)
                return JsonResponse({'result': 'logout'})

            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)

            texttospeech("If you wish to do anything else in the inbox or logout of your mail say yes or else say no.", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                texttospeech("Enter your desired action. Say unread, search, back or logout. ", file + i)
                i = i + str(1)
        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'homepage/inbox.html')



# import os
# import imaplib
# import email
# import smtplib
# import mimetypes
# import speech_recognition as sr
# import pyttsx3

# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders

# recognizer = sr.Recognizer()
# tts_engine = pyttsx3.init()

# def speak(text):
#     tts_engine.say(text)
#     tts_engine.runAndWait()

# def recognize_speech_from_mic():
#     with sr.Microphone() as source:
#         speak("Listening...")
#         audio = recognizer.listen(source)

#     try:
#         command = recognizer.recognize_google(audio)
#         return command
#     except sr.UnknownValueError:
#         speak("Sorry, I did not understand.")
#         return ""
#     except sr.RequestError:
#         speak("Sorry, there was a problem with the speech recognition service.")
#         return ""

# def login(request):
#     if request.method == 'POST':
#         email_input = request.POST.get('email')
#         password_input = request.POST.get('password')
#         request.session['email'] = email_input
#         request.session['password'] = password_input
#         return redirect('options')
#     return render(request, 'login.html')

# def options(request):
#     speak("Say read inbox, compose email, or manage inbox.")
#     command = recognize_speech_from_mic().lower()

#     if 'read' in command:
#         return redirect('read_inbox')
#     elif 'compose' in command:
#         return redirect('compose_email')
#     elif 'manage' in command:
#         return redirect('manage_inbox')
#     else:
#         speak("Command not recognized.")
#         return render(request, 'options.html')

# def compose_email(request):
#     if request.method == 'POST':
#         to_address = request.POST.get('to')
#         subject = request.POST.get('subject')
#         body = request.POST.get('body')
#         attachment = request.FILES.get('attachment')
#         email_user = request.session.get('email')
#         email_pass = request.session.get('password')

#         message = MIMEMultipart()
#         message['From'] = email_user
#         message['To'] = to_address
#         message['Subject'] = subject
#         message.attach(MIMEText(body, 'plain'))

#         if attachment:
#             fs = FileSystemStorage()
#             filename = fs.save(attachment.name, attachment)
#             file_path = fs.path(filename)

#             with open(file_path, 'rb') as attachment_file:
#                 mime_type, _ = mimetypes.guess_type(file_path)
#                 maintype, subtype = mime_type.split('/')
#                 part = MIMEBase(maintype, subtype)
#                 part.set_payload(attachment_file.read())
#                 encoders.encode_base64(part)
#                 part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
#                 message.attach(part)

#         try:
#             with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as s:
#                 s.starttls()
#                 s.login(email_user, email_pass)
#                 s.send_message(message)
#                 speak("Email sent successfully.")
#         except Exception as e:
#             speak(f"Failed to send email. {str(e)}")

#         return redirect('options')

#     return render(request, 'compose.html')

# def read_inbox(request):
#     email_user = request.session.get('email')
#     email_pass = request.session.get('password')
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(email_user, email_pass)
#     mail.select("inbox")
#     result, data = mail.search(None, "ALL")
#     mail_ids = data[0].split()
#     latest_email_ids = mail_ids[-5:]
#     emails = []

#     for num in reversed(latest_email_ids):
#         result, msg_data = mail.fetch(num, "(RFC822)")
#         raw_email = msg_data[0][1]
#         msg = email.message_from_bytes(raw_email)
#         subject = msg["subject"]
#         from_ = msg["from"]
#         body = ""

#         if msg.is_multipart():
#             for part in msg.walk():
#                 content_type = part.get_content_type()
#                 if content_type == "text/plain":
#                     body = part.get_payload(decode=True).decode()
#                     break
#         else:
#             body = msg.get_payload(decode=True).decode()

#         emails.append({"from": from_, "subject": subject, "body": body})
#         speak(f"Email from {from_}, subject: {subject}")

#     return render(request, 'inbox.html', {"emails": emails})

# def manage_inbox(request):
#     email_user = request.session.get('email')
#     email_pass = request.session.get('password')
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(email_user, email_pass)
#     mail.select("inbox")
#     result, data = mail.search(None, "ALL")
#     mail_ids = data[0].split()
#     latest_email_ids = mail_ids[-5:]
#     emails = []

#     for num in reversed(latest_email_ids):
#         result, msg_data = mail.fetch(num, "(RFC822)")
#         raw_email = msg_data[0][1]
#         msg = email.message_from_bytes(raw_email)
#         subject = msg["subject"]
#         from_ = msg["from"]
#         body = ""

#         if msg.is_multipart():
#             for part in msg.walk():
#                 content_type = part.get_content_type()
#                 if content_type == "text/plain":
#                     body = part.get_payload(decode=True).decode()
#                     break
#         else:
#             body = msg.get_payload(decode=True).decode()

#         emails.append({"id": num.decode(), "from": from_, "subject": subject, "body": body})

#     return render(request, 'manage_inbox.html', {"emails": emails})

# def delete_email(request, email_id):
#     email_user = request.session.get('email')
#     email_pass = request.session.get('password')
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(email_user, email_pass)
#     mail.select("inbox")
#     mail.store(email_id, '+FLAGS', '\\Deleted')
#     mail.expunge()
#     speak("Email deleted.")
#     return redirect('manage_inbox')
