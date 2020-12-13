from django.shortcuts import render
from django.http import HttpResponse
from .models import MyUser, PhoneOTP
import random
import requests


# Create your views here.
def send_sms(message, phone):
    url = "https://www.fast2sms.com/dev/bulk"
    payload = "sender_id=FSTSMS&message=" + message + "&language=english&route=p&numbers=" + str(phone)
    headers = {
        'authorization': "vkiOUoylIKxPEmafS2Bj3N40pzweVqYCgGtWhLQFDA1cbHdJs79rleFZjk5N8IzqA6KoXQDBG2spOVxf",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


def validate(request):
    phone_number = request.POST.get('phone')
    if len(phone_number) == 10:
        if phone_number:
            phone = str(phone_number)
            request.session['phone'] = phone
            user = MyUser.objects.filter(contact=phone)
            if user.exists():
                # if request.POST.get('forgot_password'):
                #     phone_number = request.POST.get('forgot_phone')
                phone = str(phone_number)
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(contact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        # key = old.otp
                        PhoneOTP.objects.filter(contact=phone).delete()
                        obj = PhoneOTP.objects.create(
                            contact=phone,
                            otp=key,
                            count=count,
                        )
                        obj.save()
                        old = PhoneOTP.objects.filter(contact=phone)
                        old = old.first()
                        if count > 5:
                            return HttpResponse("Limit Exceeded")
                        else:
                            old.count = count + 1
                            old.save()
                            message = "Your OTP Is " + str(key)
                            send_sms(message, phone)
                            # message = client.messages \
                            #     .create(
                            #     body="Your Password Reset OTP Is " + str(key),
                            #     from_='+15014303402',
                            #     to='+91' + phone
                            # )
                            return HttpResponse("Sent Successfully")
                    else:
                        obj = PhoneOTP.objects.create(
                            contact=phone,
                            otp=key,
                        )
                        obj.save()
                        try:
                            message = "Your OTP Is " + str(key)
                            send_sms(message, phone)
                            # message = client.messages \
                            #     .create(
                            #     body="Your Password Reset OTP Is " + str(key),
                            #     from_='+15014303402',
                            #     to='+91' + phone
                            # )
                        except Exception as e:
                            print(e)
                        return HttpResponse("Sent Successfully")
                # else:
                #     return HttpResponse("User Exists")
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(contact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        # key = old.otp
                        PhoneOTP.objects.filter(contact=phone).delete()
                        obj = PhoneOTP.objects.create(
                            contact=phone,
                            otp=key,
                            count=count,
                        )
                        obj.save()
                        old = PhoneOTP.objects.filter(contact=phone)
                        old = old.first()
                        if count > 5:
                            return HttpResponse("Limit Exceeded")
                        else:
                            old.count = count + 1
                            old.save()
                            message = "Your OTP Is " + str(key)
                            send_sms(message, phone)
                            # message = client.messages \
                            #     .create(
                            #     body="Your OTP Is " + str(key),
                            #     from_='+15014303402',
                            #     to='+91' + phone
                            # )
                            return HttpResponse("Sent Successfully")
                    else:
                        obj = PhoneOTP.objects.create(
                            contact=phone,
                            otp=key,
                        )
                        obj.save()
                        try:
                            message = "Your OTP Is " + str(key)
                            send_sms(message, phone)
                            # message = client.messages \
                            #     .create(
                            #     body="Your OTP Is " + str(key),
                            #     from_='+15014303402',
                            #     to='+91' + phone
                            # )
                        except Exception as e:
                            print(e)
                        return HttpResponse("Sent Successfully")
                else:
                    return HttpResponse("OTP Sending Error")
        else:
            return HttpResponse("No Phone Number Provided")
    else:
        return HttpResponse("Invalid Phone Length")


def ValidateOTP(request):
    phone = request.session.get('phone')
    otp_sent = request.POST.get('otp')
    if otp_sent and phone:
        old = PhoneOTP.objects.filter(phone=phone)
        if old.exists():
            old = old.first()
            otp = old.otp
            otp_time = old.date
            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            if current_time > otp_time + timedelta(minutes=1):
                return HttpResponse('OTP Expired')
            if str(otp_sent) == str(otp):
                old.validated = True
                old.save()
                if request.POST.get('forgot_password'):
                    MyUser.objects.filter(phone=phone).update(password=str(otp_sent) + "123")
                    UserInfo.objects.filter(rel=MyUser.objects.get(phone=phone)).update(password=str(otp_sent) + "123",
                                                                                        password2=str(otp_sent) + "123")
                    message = "Your Password Is " + str(otp_sent) + "123 . Please Change It Immediately."
                    send_sms(message, phone)
                    # message = client.messages \
                    #     .create(
                    #     body="Your Password Is " + str(otp_sent) + "123 . Please Change It Immediately.",
                    #     from_='+15014303402',
                    #     to='+91' + phone
                    # )
                    messages = "We Have sent Your Password On Your Registered Phone. Please Change It Immediately. "
                    links = "LogIn To Change."
                    return HttpResponse("Success")
                return HttpResponse("success")
            else:
                return HttpResponse("OTP Incorrect")
        else:
            return HttpResponse("Send Otp First")
    else:
        return HttpResponse("Please Provide Phone and OTP.")


def Register(request):
    phone = request.session.get('phone')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    address = request.POST.get('address')
    email = request.POST.get('email')
    aadhar = request.FILES.get('aadhar')
    dp = request.FILES.get('dp')
    pan = request.FILES.get('pan')
    name = request.POST.get('full_name')
    if phone and password:
        if password == password2:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    myuser = MyUser(phone=phone, password=password, name=name, email=email, profile_pic=dp)
                    myuser.save()
                    inst = MyUser.objects.get(phone=phone)
                    newuser = UserInfo(rel=inst, password2=password2, phone=phone, password=password, email=email,
                                       address=address, aadhar_card=aadhar, pan_card=pan, name=name, profile_pic=dp)
                    newuser.save()
                    try:
                        message = "New User Register with phone" + " " + str(phone) + "."
                        send_sms(message, "8887896739")
                        # message = client.messages \
                        #     .create(
                        #     body="New User Register with phone" + " " + str(phone) + ".",
                        #     from_='+15014303402',
                        #     to='+918887896739'
                        # )
                    except Exception as e:
                        print(e)
                    error_message = "Account Created Successfully. CliCk Here For "
                    error_link = "Log In"
                    return render(request, 'messages.html', {'messages': error_message, 'links': error_link})
                else:
                    error_message = "Phone Hav not Verified yet via OTP. Please Complete That Process First."
                    return render(request, 'messages.html', {'messages': error_message})
            else:
                error_message = "Please Verify Your Phone First. "
                error_link = 'Verify Here'
                return render(request, 'messages.html', {'messages': error_message, 'links': error_link})
    else:
        error_message = "Phone Or Password Details Are Not Filled Correctly. "
        error_link = "Try Again"
        return render(request, 'messages.html', {'messages': error_message, 'links': error_link})



def send_otp(phone):
    if phone:
        key = random.randint(111111, 999999)
        return key
    else:
        return False
