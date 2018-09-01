from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Match, UserE
from django.contrib.auth.models import User
import json
import time
import ast

def Index(request):

    if request.user.is_authenticated:
        user = UserE.objects.filter(user=request.user).first()

        match = Match.objects.filter(id=user.match_id.id).first()
        if request.user==match.user1:
            return render(request,'main/index.html',{"data":json.loads(match.data),"time1":int(match.time1-time.time()+match.lastTime),"user_id":user.user.id,"time2":match.time2,"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id})
        else:
            return render(request,'main/index.html',{"data":json.loads(match.data),"time1":int(match.time1-time.time()+match.lastTime),"user_id":user.user.id,"time2":match.time2,"match_user1":match.user1,"match_user2":match.user2,"match_id":user.match_id.id})

    else:
        return HttpResponseRedirect('/accounts/login/')

def checkChance(request):
    if request.user.is_authenticated:
        match_id = int(request.POST['match_id'])
        match = Match.objects.filter(id=match_id).first()
        if request.user.id == match.user1:
            dic = {}
            if(match.chance1):
                match.chance1=0
                match.save()
                dic['status'] = 1
                dic['data'] = match.data
                dic['time1'] = match.time1
                dic['time2'] = match.time2
                return HttpResponse(dic)
            return HttpResponse({'status':0})
            # return HttpResponse(match.chance1)
        elif request.user.id == match.user2:
            dic = {}
            if(match.chance2):
                match.chance2=0
                match.save()
                dic['status'] = 1
                dic['data'] = match.data
                dic['time1'] = match.time1
                dic['time2'] = match.time2
                return HttpResponse(dic)
            return HttpResponse({'status':0})
            # return HttpResponse(match.chance2)
    return HttpResponse("Not Authenticated")

def initMatch(request,user1,user2):
    match = Match()
    match.user1 = User.objects.filter(id=user1).first()
    match.user2 = User.objects.filter(id=user2).first()
    match.lastTime = int(time.time()+5000)
    data = '{"json":{"white":[{"imgPos":0,"piece":"ROOK","row":0,"col":0},{"imgPos":2,"piece":"BISHOP_1","row":4,"col":0},{"imgPos":2,"piece":"BISHOP_2","row":7,"col":0},{"imgPos":3,"piece":"KING","row":9,"col":0},{"imgPos":1,"piece":"KNIGHT_1","row":2,"col":0},{"imgPos":1,"piece":"KNIGHT_2","row":5,"col":0}],"black":[{"imgPos":0,"piece":"ROOK","row":9,"col":14},{"imgPos":2,"piece":"BISHOP_1","row":5,"col":14},{"imgPos":2,"piece":"BISHOP_2","row":2,"col":14},{"imgPos":3,"piece":"KING","row":0,"col":14},{"imgPos":1,"piece":"KNIGHT_1","row":7,"col":14},{"imgPos":1,"piece":"KNIGHT_2","row":4,"col":14}]},"smo":[0,0,0,0,0,0],"clickodd":0,"hadRotPrev":[0,0],"prevbx":null,"prevby":null,"score":[0,0],"jsonindex":null}'
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
