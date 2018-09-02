from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Match, UserE
from django.contrib.auth.models import User
import json
import time
import ast
import random
import string

def Index(request):

    if request.user.is_authenticated:

        user = UserE.objects.filter(user=request.user).first()

        match = Match.objects.filter(id=user.match_id.id).order_by('-id').first()
        if match.move == 69:
            return HttpResponseRedirect('/finished')
        if request.user==match.user1:
            myuser = "user1"
            if match.move == 0:
                chance = 0
            elif match.move == 1:
                chance = 1
            if chance == 1:
                return render(request,'main/index.html',{"data":json.loads(match.data),"time1":int(match.time1-time.time()+match.lastTime),"user_id":user.user.id,"time2":match.time2,"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id,"move":match.move,"myuser":myuser,"chance":chance})
            else:
                return render(request,'main/index.html',{"data":json.loads(match.data),"time1":match.time1,"user_id":user.user.id,"time2":int(match.time1-time.time()+match.lastTime),"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id,"move":match.move,"myuser":myuser,"chance":chance})
        else:
            myuser = "user2"
            if match.move == 1:
                chance = 0
            elif match.move == 0:
                chance = 1
            if chance ==0:
                return render(request,'main/index.html',{"data":json.loads(match.data),"time1":int(match.time1-time.time()+match.lastTime),"user_id":user.user.id,"time2":match.time2,"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id,"move":match.move,"myuser":myuser,"chance":chance})
            else:
                return render(request,'main/index.html',{"data":json.loads(match.data),"time1":match.time1,"user_id":user.user.id,"time2":int(match.time1-time.time()+match.lastTime),"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id,"move":match.move,"myuser":myuser,"chance":chance})

    else:
        return HttpResponseRedirect('/accounts/login/')

def finished(request):
    user = UserE.objects.filter(user=request.user).first()
    match = Match.objects.filter(id=user.match_id.id).order_by('-id').first()
    x = json.loads(match.data)['json']
    sw = 0
    if x['white'][0]['row']==-1:
        sw+=40
    if x['white'][1]['row']==-1:
        sw+=30
    if x['white'][2]['row']==-1:
        sw+=30
    if x['white'][3]['row']==-1:
        sw+=70
    if x['white'][4]['row']==-1:
        sw+=35
    if x['white'][5]['row']==-1:
        sw+=35
    sb = 0
    if x['black'][0]['row']==-1:
        sb+=40
    if x['black'][1]['row']==-1:
        sb+=30
    if x['black'][2]['row']==-1:
        sb+=30
    if x['black'][3]['row']==-1:
        sb+=70
    if x['black'][4]['row']==-1:
        sb+=35
    if x['black'][5]['row']==-1:
        sb+=35

    return HttpResponse("Game is Over<br>White : " + match.user1.username + " : " +str(sw) +"<br>Black : " + match.user2.username + " : " +str(sb)  )

def endgame(request):
    if request.user.is_authenticated:
        match_id = int(request.POST['match_id'])
        match = Match.objects.filter(id=match_id).first()
        match.move=69
        match.data = request.POST['data']
        match.save()
        return HttpResponse(json.dumps({'status':69}))
    return HttpResponse("Not Authenticated")


def checkChance(request):
    if request.user.is_authenticated:
        match_id = int(request.POST['match_id'])
        match = Match.objects.filter(id=match_id).first()
        if match.move==69:
            return HttpResponse(json.dumps({'status':69}))
        if request.user.id == match.user1.id:
            dic = {}
            if(match.chance1):
                match.chance1=0
                match.move=1;
                match.save()
                dic['status'] = 1
                dic['move'] = 1
                dic['move'] = match.move
                dic['data'] = json.loads(match.data)
                dic['time1'] = int(match.time1-time.time()+match.lastTime)
                dic['time2'] = match.time2
                return HttpResponse(json.dumps(dic))
            return HttpResponse(json.dumps({'status':0}))
            # return HttpResponse(match.chance1)
        elif request.user.id == match.user2.id:
            dic = {}
            if(match.chance2):
                match.chance2=0
                match.move=0;
                match.save()
                dic['status'] = 1
                dic['data'] = json.loads(match.data)
                dic['move'] = match.move
                dic['time1'] = match.time1
                dic['time2'] = int(match.time2-time.time()+match.lastTime)
                return HttpResponse(json.dumps(dic))
            return HttpResponse(json.dumps({'status':0}))
            # return HttpResponse(match.chance2)
    return HttpResponse("Not Authenticated")

def initMatch(request,user1,user2):
    match = Match()
    match.user1 = User.objects.filter(id=user1).first()
    match.user2 = User.objects.filter(id=user2).first()
    match.lastTime = int(time.time())
    data = '{"json":{"white":[{"imgPos":0,"piece":"ROOK","row":0,"col":0},{"imgPos":2,"piece":"BISHOP_1","row":3,"col":0},{"imgPos":2,"piece":"BISHOP_2","row":6,"col":0},{"imgPos":3,"piece":"KING","row":9,"col":0},{"imgPos":1,"piece":"KNIGHT_1","row":2,"col":0},{"imgPos":1,"piece":"KNIGHT_2","row":7,"col":0}],"black":[{"imgPos":0,"piece":"ROOK","row":9,"col":14},{"imgPos":2,"piece":"BISHOP_1","row":3,"col":14},{"imgPos":2,"piece":"BISHOP_2","row":6,"col":14},{"imgPos":3,"piece":"KING","row":0,"col":14},{"imgPos":1,"piece":"KNIGHT_1","row":7,"col":14},{"imgPos":1,"piece":"KNIGHT_2","row":2,"col":14}]},"smo":[0,0,0,0,0,0],"clickodd":0,"hadRotPrev":[0,0],"prevbx":null,"prevby":null,"score":[0,0],"jsonindex":null}'
    match.data = data
    match.save()
    user1e = UserE.objects.filter(user=match.user1).first()
    if user1e is None:
        user1e = UserE()
        user1e.user = User.objects.filter(id=user1).first()
    user1e.match_id = match
    user1e.save()
    user2e = UserE.objects.filter(user=match.user2).first()
    if user2e is None:
        user2e = UserE()
        user2e.user = User.objects.filter(id=user2).first()
    user2e.match_id = match
    user2e.save()
    return HttpResponse("done")

def createMatches(request):
    x = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
    # x = [3,5,4,6,7,9,8,10,11,13,12,14,15,17,16,18,19,21,20,22,23,25,24,26,27,29,28,30,31,33,32,34,35,37,36,38,39,41,40,42,43,45,44,46,47,49,48,50]
    # x = [3,27,4,49,5,48,6,47,7,46,8,45,9,44,10,43,11,42,12,41,13,40,14,39,15,38,16,37,17,36,18,35,19,34,20,33,21,32,22,31,23,30,24,29,25,28,26,50]
    # x = [3,6,4,5,7,10,8,9,11,14,12,13,15,18,16,17,19,22,20,21,23,26,24,25,27,30,28,29,31,34,32,33,35,38,36,37,39,42,40,41,43,46,44,45,47,50,48,49]
    i = 0
    for j in range(0,len(x)//2):
        match = Match()
        if (i%5)%2 == 1:
            match.user1 = User.objects.filter(id=x[i]).first()
            match.user2 = User.objects.filter(id=x[i+1]).first()
        else:
            match.user1 = User.objects.filter(id=x[i+1]).first()
            match.user2 = User.objects.filter(id=x[i]).first()
        match.lastTime = int(time.time())
        match.time1 = 900
        match.time2 = 900
        data = '{"json":{"white":[{"imgPos":0,"piece":"ROOK","row":0,"col":0},{"imgPos":2,"piece":"BISHOP_1","row":3,"col":0},{"imgPos":2,"piece":"BISHOP_2","row":6,"col":0},{"imgPos":3,"piece":"KING","row":9,"col":0},{"imgPos":1,"piece":"KNIGHT_1","row":2,"col":0},{"imgPos":1,"piece":"KNIGHT_2","row":7,"col":0}],"black":[{"imgPos":0,"piece":"ROOK","row":9,"col":14},{"imgPos":2,"piece":"BISHOP_1","row":3,"col":14},{"imgPos":2,"piece":"BISHOP_2","row":6,"col":14},{"imgPos":3,"piece":"KING","row":0,"col":14},{"imgPos":1,"piece":"KNIGHT_1","row":7,"col":14},{"imgPos":1,"piece":"KNIGHT_2","row":2,"col":14}]},"smo":[0,0,0,0,0,0],"clickodd":0,"hadRotPrev":[0,0],"prevbx":null,"prevby":null,"score":[0,0],"jsonindex":null}'
        match.data = data
        match.save()
        user1e = UserE.objects.filter(user=match.user1).first()
        if user1e is None:
            user1e = UserE()
            user1e.user = User.objects.filter(id=match.user1.id).first()
        user1e.match_id = match
        user1e.save()
        user2e = UserE.objects.filter(user=match.user2).first()
        if user2e is None:
            user2e = UserE()
            user2e.user = User.objects.filter(id=match.user2.id).first()
        user2e.match_id = match
        user2e.save()
        i+=2
    return HttpResponse("Initialized.")

def createUsers(request):
    resp=""
    rollNos=["J"+str(x) for x in range(48,49)]
    if request.user.is_authenticated:
        for r in rollNos:
            passwd=''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            user,created = User.objects.get_or_create(username=str(r),email=str(r), password=passwd)
            if(created):
              resp += "Created: "+str(r) + " :\t"+ passwd
            else:
              resp += "Already exists: "+str(r)
            resp+="\n"
            user = User.objects.filter(username=r).first()
            user.set_password(passwd)
            resp+=r+" "+passwd
            resp+="<br>"
            user.save()     
            # data = TableSet.objects.filter(user=user).first()
            # if data is None:
              # df = load_data_init_train()
              # cre = Credits()
              # cre.user = user
              # cre.save()
              # dat = TableSet()
              # dat.user = user
              # dat.data = df.to_string()
              # dat.save()
              # create_log(user,"Intialized.")
        return HttpResponse(resp)
    else:
        return HttpResponse("Not Logged IN")


def playMove(request):
    if request.user.is_authenticated:
        match_id = int(request.POST['match_id'])
        match = Match.objects.filter(id=match_id).first()
        if request.user.id == match.user1.id:
            match.time1 -= (int(time.time()) - match.lastTime)
            match.chance2 = 1
        elif request.user.id == match.user2.id:
            match.time2 -= (int(time.time()) - match.lastTime)
            match.chance1 = 1
        else:
            return HttpResponse("not your match")
        match.lastTime = int(time.time())
        match.data = request.POST['data']
        match.save()
        return HttpResponse(match.chance2)
    return HttpResponse("Not Authenticated")
