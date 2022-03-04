import re
from django.shortcuts import render,redirect
from django.utils.timezone import datetime
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from django.conf import settings
from projectapp.models import admn,playerreg,regcoachh,venue,payment,report,time,video,game,msgg,game,team,game_time,team_category,game_time
# Create your views here.
def main_page(request):
    return render(request,'index.html')
def home(request):
    return render(request,'index.html')
def admin_login(request):
    return render(request,'admin_login.html')
def player_login(request):
    return render(request,'player_login.html')
def coach_login(request):
    return render(request,'coach_login.html')
def addm(request):
    return render(request,'admin_home.html')
def coach(request):
    return render(request,'index2.html')
def admin_log(request):
    try:
        m = admn.objects.get(aname=request.POST['name'])
        if m.apassword == request.POST['password']:
            request.session['admin_id'] = m.aname
            return redirect(addm)
        else:
            return redirect(admin_login)
    except:
        return redirect(home)
#
def player_log(request):
        try :
            x = playerreg.objects.get(rname=request.POST['name'])
            if x.rpassword == request.POST['password']:
                request.session['player_id'] = x.rname

                return render(request,'index3.html')
            else:
                return redirect(player_login)
        except :
            return redirect(home)

def coach_log(request):
        try:
            m = regcoachh.objects.get(cname=request.POST['name'])
            if m.cpassword == request.POST['password'] and m.status=="accept":
                request.session['coach_id'] = m.cname
                return redirect(coach)
            else:
                return redirect(coach_login)

        except :
            return redirect(home)
def coachreg(request):
    import os
     # if (request.POST,request.Files):
    k = request.POST['coachid']
    a = request.POST['name']
    b = request.POST['sports']
    c = request.POST['phone']
    d = request.POST['place']
    e = request.POST['dob']
    f = request.POST['qualification']
    g = request.POST['fee']
    z = request.FILES['image']
    print(z)
    h = request.POST['email']
    i = request.POST['password']

    if re.match(r"^[6789]{1}\d{9}$", c):
        if re.match(r'[\w-]{1,20}@\w{2,20}\.\w{2,3}$', h):
            j = regcoachh(cid=k, cname=a, csports=b, cphone=c, cplace=d, cdob=e, cqualification=f, cfee=g,ccertificate=z,cemail=h, cpassword=i,status='pending')
            j.save()
            print(j)

            return home(request)

        else:
            return render(request,"regcoach.html",{"s":'!!!Invalid EmailAddress!!!'})
    else:
        return render(request, "regcoach.html", {"s":'!!!phone number!!!'})

def creg(request):
    return render(request,'regcoach.html',{'message':"password incorrect"})
def fun1(request):
    import os
    q=request.POST['gme']
    z = request.POST['plid']
    a = request.POST['name']
    b = request.POST['phone']
    c = request.POST['place']
    d = request.POST['dob']
    e = request.POST['height']
    f = request.POST['weight']
    g = request.POST['email']
    h = request.POST['password']
    if re.match(r"^[6789]{1}\d{9}$", b):
        if re.match(r'[\w-]{1,20}@\w{2,20}\.\w{2,3}$', g):
            i = playerreg(rid=z, rname=a, rphone=b, rplace=c, rdob=d, height=e,gid=q, weight=f, remail=g, rpassword=h)
            i.save()
            return home(request)
        else:
            return render(request,"register.html",{"s":'!!!Invalid EmailAddress!!!'})
    else:
        return render(request, "register.html", {"s": '!!!Invalid phone number!!!'})
def preg(request):
    g=game.objects.all()
    return render(request,'register.html',{'message':"password incorrect",'game':g})
def plogout(request):
    try:
        del request.session['player_id']
    except:
        pass
    return redirect(home)
def clogout(request):
    try:
        del request.session['coach_id']
    except:
        pass
    return redirect(home)
# def venueadd(request):
#     a = request.POST['place']
#     b = request.POST['description']
#     c = request.POST['date']
#     d = request.POST['time']
#     e=venue(vplace=a,vdescription=b,vdate=c,vtime=d)
#     e.save()
#     return redirect(addm)
# def addvenuee(request):
#     return render(request,'addvenue.html')
def coachmanage(request):
    user=regcoachh.objects.all()
    return render(request,'managecoach.html',{'user':user})
def admin_accept_coach(request):
    if request.method=="POST":
        cid=request.POST['id']
        c=regcoachh.objects.filter(cid=cid).update(status='accept')
        coach_id=regcoachh.objects.get(cid=cid)
        import smtplib
        from email.mime.text import MIMEText
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('projectsriss2020@gmail.com','messageforall')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your request is accepted ")
        msg['Subject'] = 'Verification'
        msg['To'] = coach_id.cemail
        msg['From'] = 'projectsriss2020@gmail.com'
        try:
            gmail.send_message(msg)
        except Exception as e:

            print("COULDN'T SEND EMAIL", str(e))
        return redirect(coachmanage)
    return render(request,'managecoach.html',{'alert_flag': True})
def midd(request):
    id = request.POST['id']
    user = regcoachh.objects.filter(cid=id).update(status='accept')
    return render(request,'editm.html',{'user':user})
def editm(request):
    c1id=request.POST['coachid']
    name = request.POST['name']
    sports = request.POST['sports']
    qualification = request.POST['qualification']
    place = request.POST['place']
    phone = request.POST['phone']
    email = request.POST['email']
    fee = request.POST['fee']
    regcoachh.objects.filter(cid=c1id).update(cname=name,csports=sports,cqualification=qualification,cplace=place,cphone=phone,cemail=email,cfee=fee)
    return redirect(coachmanage)
def deletes(request):
    id = request.POST['id']
    regcoachh.objects.filter(cid=id).delete()
    return redirect(coachmanage)
def paymentview(request):
    user=payment.objects.all()
    return render(request,'payments.html',{'user':user})
def reportview(request):
    user = report.objects.all()
    return render(request,'reportview.html',{'user':user})
def searchp(request):
    return render(request,'searchbox.html')
def search(request):
        user = playerreg.objects.filter(rname=request.POST['name'])
        return render(request, 'pregview.html', {'user': user})
def admlogout(request):
    try:
        del request.session['admin_id']
    except:
        pass
    return redirect(main_page)
def addtime(request):
    return render(request,'addtime.html')
def timeschedule(request):
    f = request.POST['id']
    a = request.POST['sports']
    b = request.POST['date']
    c = request.POST['timee']
    d = request.POST['time1']
    e = time(tid=f,gameid=a,tdate=b,startingtime=c,endingtime=d)
    e.save()
    return redirect(coach)
def updatetime(request):
    user = time.objects.all()
    return render(request,'updatetime.html',{'user':user})
def tidd(request):
    id = request.POST['id']
    user = time.objects.filter(tid=id)
    return render(request,'updatet.html',{'user': user})
def deletes1(request):
    id = request.POST['id']
    time.objects.filter(tid=id).delete()
    return redirect(updatetime)
def tupdate(request):
    t1id = request.POST['id']
    sports = request.POST['sports']
    #date = request.POST['date']
    timee = request.POST['timee']
    time1 = request.POST['time1']
    time.objects.filter(tid=t1id).update(gameid=sports,startingtime=timee,endingtime=time1)
    return redirect(updatetime)
def reportt(request):
    return render(request,'report.html')
def addreport(request):
    a = request.POST['playerid']
    b = request.POST['reportid']
    c = request.POST['report']
    d = report(tid=a,playerid=b,preport=c)
    d.save()
    return redirect(coach)
def uploadvideo(request):
    import os
    a = request.POST['id']
    b = request.FILES['video']
    filename, file_extension = os.path.splitext(str(b))
    c = request.POST['description']
    d = request.POST['date']
    if file_extension == '.mp4' or file_extension == '.mov' or file_extension == '.avi' or file_extension == '.wmv' or file_extension == '.flv' or file_extension == '.webm':
        e = video(videoid=a, videos=b, description=c, videodate=d)
        e.save()

        return coach(request)
    else:
        return render(request, "video.html", {"s": '!!!Invalid video formate!!!'})
def videoo(request):
    return render(request,'video.html')
def addgame(request):
    return render(request,'addgame.html')
def gameadd(request):
    g = request.POST['id']
    a = request.POST['sports']
    b = request.POST['nplayers']
    c = request.POST['duration']
    d = request.POST['description']
    e = request.POST['amount']
    f = game(gid=g,games=a,nofplayers=b,duration=c,gdescription=d,amount=e)
    f.save()
    return redirect(coach)
def updategame(request):
    user = game.objects.all()
    return render(request, 'updategame.html', {'user': user})
def gidd(request):
    id = request.POST['id']
    user = game.objects.filter(gid=id)
    return render(request,'updateg.html',{'user': user})
def deletes2(request):
    id = request.POST['id']
    game.objects.filter(gid=id).delete()
    return redirect(updategame)
def gupdate(request):
    g1id = request.POST['id']
    sports = request.POST['sports']
    nplayers = request.POST['nplayers']
    duration = request.POST['duration']
    description = request.POST['description']
    amount = request.POST['amount']
    game.objects.filter(gid=g1id).update(games=sports,nofplayers=nplayers,duration=duration,gdescription=description,amount=amount)
    return redirect(updategame)
def msgv(request):
    id=request.session['coach_id']
    m=msgg.objects.filter(coach=id)
    return render(request,'msgview.html',{'user':m})

def deletes3(request):
    id = request.POST['id']
    msgg.objects.filter(mname=id).delete()
    return redirect(msgv)
def pfee(request):
    return render(request,'playerpayment.html')
def playeramount(request):
    a = request.POST['playerid']
    b = request.POST['game']
    c = request.POST['amount']
    d = request.POST['date']
    e = request.POST['time']
    f = payment(rid=a,gameid=b,pstatus=c, pdate=d, ptime=e)
    f.save()
    return redirect(coach)
def clogout(request):
    try:
        del request.session['coach_id']
    except:
        pass
    return redirect(main_page)
def emergancy(request):
    id = request.session['player_id']
    t = team.objects.get(players=id)
    x=t.coach_name
    print(x)
    return render(request,'emergancy.html',{'ch':x})
def emgmsg(request):
    a = request.POST['pname']
    b = request.POST['msg']
    d= request.POST['cch']
    c = msgg(mname=a,msg=b,coach=d)
    c.save()
    return redirect(player)
def player(request):
    return render(request,'index3.html')
def gameaddview(request):
    user = game.objects.all()
    return render(request, 'gameaddview.html', {'user': user})
def playertimeview(request):
    id=request.session['player_id']
    t=team.objects.filter(players=id)
    print(t)
    print(id)
    q=team.objects.get(players=id)
    print(q)
    x=q.team_name
    print(x)
    gt = game_time.objects.filter(team_name=x)
    print(gt)
    return render(request,'ptimeview.html',{'tym':gt})
def videoview(request):
    user = video.objects.all()
    return render(request,'videoview.html',{'user':user})
def plogout(request):
    try:
        del request.session['player_id']
    except:
        pass
    return redirect(main_page)
def admin_add_team(request):
    c=regcoachh.objects.all()
    p=playerreg.objects.all()
    t=team_category.objects.all()
    return render(request,'admin_add_team.html',{'ch':c,'pl':p,'tm':t})

def add_team(request):
    a=request.POST['tname']
    b=request.POST['coach']
    c=request.POST['player']
    q=team(team_name=a,coach_name=b,players=c)
    q.save()
    return redirect(addm)

def view_team(request):
    id = request.session['coach_id']
    t = team.objects.filter(coach_name=id)
    return render(request, 'coach_view_team.html', {'tm':t})

def coach_add_time(request):
    return render(request,'coach_add_time.html')
def schedule_time(request):
    x=request.POST['tid']
    z=request.POST['tname']
    a=request.POST['stime']
    b=request.POST['etime']
    q=game_time(game_time_id=x,team_name=z,start_time=a,end_time=b)
    q.save()
    return redirect(view_team)

def player_view_team(request):
    id = request.session['player_id']
    t=team.objects.filter(players=id)
    return render(request,'player_view_team.html', {'tm':t})
