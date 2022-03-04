from django.db import models

# Create your models here.
class admn(models.Model):
    aname=models.CharField(max_length=20)
    apassword = models.CharField(max_length=20)
class regcoachh(models.Model):
    cid=models.IntegerField(primary_key=True)
    cname=models.CharField(max_length=20)
    csports=models.CharField(max_length=20)
    cdob=models.DateField()
    cqualification=models.CharField(max_length=20)
    cplace=models.CharField(max_length=30)
    cphone=models.IntegerField()
    ccertificate=models.FileField()
    cemail=models.EmailField()
    cfee=models.BigIntegerField()
    cpassword=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
class venue(models.Model):
    vid=models.IntegerField(primary_key=True)
    vplace=models.CharField(max_length=30)
    vdescription=models.CharField(max_length=80)
    vdate=models.DateField()
    vtime=models.TimeField()
class payment(models.Model):
    rid=models.IntegerField(primary_key=True)
    gameid=models.CharField(max_length=20)
    pdate=models.DateField()
    ptime=models.TimeField()
    pstatus=models.CharField(max_length=10)
class time(models.Model):
    tid=models.IntegerField(primary_key=True)
    gameid=models.CharField(max_length=20)
    tdate=models.DateField()
    startingtime=models.TimeField()
    endingtime=models.TimeField()
class report(models.Model):
    tid=models.IntegerField(primary_key=True)
    playerid=models.IntegerField()
    preport=models.CharField(max_length=100)
class video(models.Model):
    videoid=models.IntegerField(primary_key=True)
    videos=models.FileField()
    description=models.CharField(max_length=100)
    videodate=models.DateField()
class game(models.Model):
    gid=models.IntegerField(primary_key=True)
    games=models.CharField(max_length=20)
    nofplayers=models.IntegerField()
    duration=models.IntegerField()
    gdescription=models.CharField(max_length=100)
    amount=models.IntegerField()
class playerreg(models.Model):
    rid=models.IntegerField(primary_key=True)
    rname=models.CharField(max_length=20)
    remail=models.EmailField()
    height=models.IntegerField()
    gid=models.CharField(max_length=100)
    weight=models.IntegerField()
    rdob=models.DateField()
    rplace=models.CharField(max_length=30)
    rphone=models.IntegerField()
    rpassword=models.CharField(max_length=20)
class msgg(models.Model):
    mname=models.CharField(max_length=20)
    msg=models.CharField(max_length=30)
    coach=models.CharField(max_length=100)

class team(models.Model):
    team_name=models.CharField(max_length=100)
    coach_name = models.CharField(max_length=100)
    players=models.CharField(max_length=100)
class team_category(models.Model):
    team_name=models.CharField(max_length=100)

class game_time(models.Model):
    game_time_id=models.IntegerField()
    team_name=models.CharField(max_length=100)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()















