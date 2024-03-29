import json
from random import randint
import random
import datetime
import time
import csv

import numpy
from numpy import arange, array, ones
from scipy import stats

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from InvestGame.settings import BASE_DIR, DATA_ADDR, INFO_STORE
from django.core.files.storage import FileSystemStorage
import os
from .models import User
from .models import HoltLaury
from .models import Gamble
from .models import Investment
from .models import Pretest
from .models import Training
from .models import Thankyou



def compare(request):

    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
    (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        user = User.objects.get(username=umid)
        investment = user.investment_set.all()[0]
        user_invested = investment.invested
        user_guess_returned = investment.returned0
        respondent = investment.respondent
        data = {}
        data_path = os.path.join(DATA_ADDR, "ans.json")
        with open(data_path) as json_file:
            data = json.load(json_file)
        real_returned = data[respondent][str(user_invested)]
        investment.returned1 = real_returned
        user.investment_set.update(
                    returned1=real_returned)
        user_received = real_returned
        guess_flag = "not within"
        bonus = 0
        if abs(real_returned - user_guess_returned) <= 1:
            user_received += 2
            guess_flag = "within"
            bonus = 2
        user_received += (5-user_invested)
        user_left = (5-user_invested)
        investment.returned2 = user_received
        user.investment_set.update(
                    returned2=user_received)
        user.save()
        context = { 'umid': umid, 'invested': user_invested, 'guess_returned':user_guess_returned, 'real_returned': real_returned, 'received': user_received, 'respondent': respondent, 'guess_flag': guess_flag, 'nodata' : False, 'user_left': user_left, 'bonus': bonus}
        return render(request, 'games/compare.html', context)

@ensure_csrf_cookie
def question0(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
    context = { 'umid': umid, 'nodata' : False}
    return render(request, 'games/Question0.html', context)

@ensure_csrf_cookie
def question01(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
    context = { 'umid': umid, 'nodata' : False}
    return render(request, 'games/Question0_1.html', context)

@ensure_csrf_cookie
def question0_store(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = User.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q1answer = request.POST['question1']

                flag = 0
                if investment.q1answer == " ":
                    flag = 1
                    user.investment_set.update(q1answer= q1answer)

                investment = user.investment_set.all()[0]
                q1answer = investment.q1answer

                if flag == 1:
                    userinfo = {"umid": umid, "user_invested": investment.invested, "user_guess_returned": investment.returned0,
                    "respondent": investment.respondent, "respondent_returned": investment.returned1, "user_received" : investment.returned2, "question1": q1answer}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'w+') as f:
                        json.dump(userinfo, f)
                response = HttpResponse(q1answer)
                return response


@ensure_csrf_cookie
def question01_store(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = User.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q2answer = request.POST['question2']
                q3answer = request.POST['question3']
                q4answer = request.POST['question4']
                flag = 0
                if investment.q2answer == " ":
                    flag = 1
                    user.investment_set.update(q2answer= q2answer)
                if investment.q3answer == " ":
                    user.investment_set.update(q3answer= q3answer)
                if investment.q4answer == " ":
                    user.investment_set.update(q4answer= q4answer)
                investment = user.investment_set.all()[0]
                # q2answer = investment.q2answer
                # q3answer = investment.q3answer
                # q4answer = investment.q4answer
                if flag == 1:
                    userinfo = {"question2": q2answer, "question3": q3answer, "question4": q4answer}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'a') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response


@ensure_csrf_cookie
def question1(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'games/Question1.html', context)


@ensure_csrf_cookie
def question1_store(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = User.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q5answer = request.POST['question5']
                q5type = request.POST['questiontype']

                flag = 0
                if investment.q5answer == " ":
                    flag = 1
                    user.investment_set.update(q5answer= q5answer)
                if investment.q5type == -1:
                    user.investment_set.update(q5type= q5type)


                investment = user.investment_set.all()[0]
                q5answer = investment.q5answer
                q5type = investment.q5type

                if flag == 1:                
                    userinfo = {"question5": q5answer, 'questiontype': q5type}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'a') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response


@ensure_csrf_cookie
def question2(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'games/Question2.html', context)


def finish(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                context = { 'umid': umid, 'nodata' : False}
                return render(request, 'games/finish.html', context)

@ensure_csrf_cookie
def respondent_store(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                print("fdgfds")
                umid = request.session['umid']
                user = User.objects.get(username=umid)
                if user.investment_set.count() == 0:
                    user.investment_set.create(invested=0,
                        startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                        finishedinvested=datetime.datetime.now())
                if user.investment_set.count() != 0:
                    investment = user.investment_set.all()[0]                    
                    respondent = request.POST['respondent']
                    if investment.respondent == " ":
                        user.investment_set.update(respondent= respondent)
                    else:
                        respondent = investment.respondent
                    response = HttpResponse(respondent)
                    return response


@ensure_csrf_cookie
def question2_store(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
                user = User.objects.get(username=umid)
                investment = user.investment_set.all()[0]
                q6answer = request.POST['question6']
                q7answer = request.POST['question7']
                q8answer = request.POST['question8']
                q9answer = request.POST['question9']
                q10answer = request.POST['question10']
                q11answer = request.POST['question11']
                q12answer = request.POST['question12']
                q13answer = request.POST['question13']
                q14answer = request.POST['question14']
                q15answer = request.POST['question15']
                print("dfsdfsdfs")
                print(q6answer)
                flag = 0
                if investment.q6answer == " ":
                    flag = 1
                    user.investment_set.update(q6answer= q6answer)
                if investment.q7answer == " ":
                    user.investment_set.update(q7answer= q7answer)
                if investment.q8answer == " ":
                    user.investment_set.update(q8answer= q8answer)
                if investment.q9answer == " ":
                    user.investment_set.update(q9answer= q9answer)
                if investment.q10answer == " ":
                    user.investment_set.update(q10answer= q10answer)
                if investment.q11answer == " ":
                    user.investment_set.update(q11answer= q11answer)
                if investment.q12answer == " ":
                    user.investment_set.update(q12answer= q12answer)
                if investment.q13answer == " ":
                    user.investment_set.update(q13answer= q13answer)
                if investment.q14answer == " ":
                    user.investment_set.update(q14answer= q14answer)
                if investment.q15answer == " ":
                    user.investment_set.update(q15answer= q15answer)

                investment = user.investment_set.all()[0]
                q6answer = investment.q6answer
                q7answer = investment.q7answer
                q8answer = investment.q8answer
                q9answer = investment.q9answer
                q10answer = investment.q10answer
                q11answer = investment.q11answer
                q12answer = investment.q12answer
                q13answer = investment.q13answer
                q14answer = investment.q14answer
                q15answer = investment.q15answer

                if flag == 1:
                    userinfo = {"question6": q6answer, "question7": q7answer, "question8": q8answer, "question9": q9answer, "question10": q10answer, "question11": q11answer, "question12": q12answer, "question13": q13answer, "question14": q14answer, "question15": q15answer}
                    filename = "user" + umid
                    path= os.path.join(INFO_STORE, filename+ ".json")
                    with open(path, 'a') as f:
                        json.dump(userinfo, f)
                response = HttpResponse()
                return response





@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        umid = request.GET.get("id")
        # umid = time.time()
        user, created = User.objects.get_or_create(username=umid)
        request.session['umid'] = user.username
        print(request.session['umid'])

    return welcome(request)

def logout(request):
    del request.session['umid']
    return welcome(request)

def welcome(request):
    # if ('REMOTE_USER' in request.META or request.session.get('umid', False)):
    #     if ('REMOTE_USER' in request.META):
    #         umid = request.META['REMOTE_USER']
    #     if (request.session.get('umid', False)):
    #         umid = request.session['umid']
    #     user, created = User.objects.get_or_create(username=umid)
    #     user.version = "AfterExperiment"
    #     user.save()
    #     request.session['startedStudy'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
    # else:
    if request.method == 'GET':
        umid = request.GET.get("id")
        # umid = time.time()
        user, created = User.objects.get_or_create(username=umid)
        request.session['umid'] = user.username
        loginid = ""
        context = { 'umid': loginid, 'welcomepage': 1}
        return render(request, 'games/Welcome.html', context)
    else:
        umid = request.session['umid']
        context = { 'umid': umid, 'welcomepage': 1}
        return render(request, 'games/Welcome.html', context)

@ensure_csrf_cookie
def pretest(request, question):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        user = User.objects.get(username=umid)
        if user.pretest_set.count() != 0:
            if question == "":
                question = "1"
            question = int(question)
            pretest = user.pretest_set.all()[0]
            for i in range(1, question + 1):
                if i == 1:
                    answer = pretest.question1
                    correct = pretest.correct1
                elif i == 2:
                    answer = pretest.question2
                    correct = pretest.correct2
                elif i == 3:
                    answer = pretest.question3
                    correct = pretest.correct3
                elif i == 4:
                    answer = pretest.question4
                    correct = pretest.correct4
                elif i == 5:
                    answer = pretest.question5
                    correct = pretest.correct5
                elif i == 6:
                    answer = pretest.question6
                    correct = pretest.correct6
                elif i == 7:
                    answer = pretest.question7
                    correct = pretest.correct7
                if answer == -1:
                    question = i
                    context = { 'umid': umid, 'answer':answer, 'question':question, 'welcomepage':1 }
                    return render(request, 'games/Pretest.html', context)
            context = { 'umid': umid, 'answer':answer, 'question':question, 'correct':correct, 'welcomepage':1 }
            return render(request, 'games/Pretest.html', context)

        context = { 'umid': umid, 'question':1, 'welcomepage':1 }
        return render(request, 'games/Pretest.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)



@ensure_csrf_cookie
def investment(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        user = User.objects.get(username=umid)
        gameNum = 1
        invested = 0
        if user.investment_set.count() == 0:
            user.investment_set.create(invested=invested,
                startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                finishedinvested=datetime.datetime.now())

        if user.investment_set.count() != 0:
            investment = user.investment_set.all()[0]
            invested = investment.invested
            respondent = investment.respondent
            context = { 'umid': umid, 'invested':invested, 'gameNum':gameNum, 'respondent':respondent }
            return render(request, 'games/Trust Game.html', context)
    
        context = { 'umid': umid, 'gameNum':gameNum, 'respondent':respondent}
        return render(request, 'games/Trust Game.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def investmentSubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('invested' in request.POST and request.POST['invested'] != ''):
                invested = request.POST['invested']
                user = User.objects.get(username=umid)
                if user.investment_set.count() == 0:
                    user.investment_set.create(invested=invested,
                        startedinvested=datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p'),
                        finishedinvested=datetime.datetime.now())
                else:
                    investment = user.investment_set.all()[0]  
                    if investment.doneinvest == -1:
                        user.investment_set.update(invested=invested, doneinvest=1)
            return redirect('../returning/')    
    return render(request, 'games/welcome.html')

@ensure_csrf_cookie
def returned(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        request.session['started'] = datetime.datetime.now().strftime("%b %d %Y %I:%M:%S %p")
        user = User.objects.get(username=umid)
        gameNum = 2
        part = 6
        returned = 0
        investment = user.investment_set.all()[0]
        invested = investment.invested
        respondent = investment.respondent
        # print(respondent)

        context = { 'umid': umid, 'invested': invested, 'returned':returned, 'part':part, 'gameNum':gameNum, 'respondent': respondent}
        return render(request, 'games/Trust Game.html', context)



    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def returnedSubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('returned' in request.POST and request.POST['returned'] != '' and
             'part' in request.POST and request.POST['part'] != ''):
                returned = int(request.POST['returned'])
                part = int(request.POST['part'])
                user = User.objects.get(username=umid)
                investment = user.investment_set.all()[0]  
                if investment.donereturn == -1:
                    user.investment_set.update(returned0=returned, donereturn=1)
                return redirect('../compare')
    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

@ensure_csrf_cookie
def final(request):
    if request.method == 'POST':
        requestPost = json.loads(request.body.decode('utf-8'))
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('returned' in requestPost and requestPost['returned'] != ''):
                returned = int(requestPost['returned'])
                part = 7
                user = User.objects.get(username=umid)
                gameNum = 1
                if user.firstgame == "investment":
                    gameNum = 1
                elif user.secondgame == "investment":
                    gameNum = 2
                elif user.thirdgame == "investment":
                    gameNum = 3
                if user.investment_set.count() != 0:
                    investment = user.investment_set.all()[0]
                    if investment.otherreturned == -1 and investment.otherinvested == -1:
                        for i in range(2, part + 1):
                            if i == 2:
                                returned = investment.returned0
                            elif i == 3:
                                returned = investment.returned1
                            elif i == 4:
                                returned = investment.returned2
                            elif i == 5:
                                returned = investment.returned3
                            elif i == 6:
                                returned = investment.returned4
                            elif i == 7:
                                returned = int(requestPost['returned'])
                                investment.returned5 = returned
                                investment.startedreturned5 = datetime.datetime.strptime(request.session['started'], '%b %d %Y %I:%M:%S %p')
                                investment.finishedreturned5 = datetime.datetime.now()
                                investment.save()
                            if returned == -1:
                                part = i
                                context = { 'umid': umid, 'returned':returned, 'part':part, 'gameNum':gameNum }
                                return render(request, 'games/Trust Game.html', context)
                        
                        otherPlayer = None
                        otherPlayersComparison = Investment.objects.filter(otherreturned=-1).filter(otherinvested=-1)
                        otherPlayers = Investment.objects.filter(user__version='Pilot').exclude(user=user).order_by('?')
                        for other in otherPlayers:
                            if other.invested != -1 and other.returned5 != -1 and not other in otherPlayersComparison:
                                otherPlayer = other
                                break
                        if otherPlayer == None:
                            return JsonResponse({ 'found':0 })
                        InvestOrReturn = random.getrandbits(1)
                        if InvestOrReturn:
                            investAmount = investment.invested
                            if investAmount == 0:
                                returnAmount = otherPlayer.returned0
                            elif investAmount == 1:
                                returnAmount = otherPlayer.returned1
                            elif investAmount == 2:
                                returnAmount = otherPlayer.returned2
                            elif investAmount == 3:
                                returnAmount = otherPlayer.returned3
                            elif investAmount == 4:
                                returnAmount = otherPlayer.returned4
                            elif investAmount == 5:
                                returnAmount = otherPlayer.returned5
                            investment.otherreturned = returnAmount
                            # otherPlayer.otherinvested = investAmount

                            investment.points = 5 - investAmount + returnAmount
                            # otherPlayer.points = 5 + (3 * investAmount) - returnAmount

                        else:
                            investAmount = otherPlayer.invested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            # otherPlayer.otherreturned = returnAmount
                            investment.otherinvested = investAmount

                            # otherPlayer.points = 5 - investAmount + returnAmount
                            investment.points = 5 + (3 * investAmount) - returnAmount

                        investment.otheruser = otherPlayer.user
                        # otherPlayer.otheruser = user
                        investment.save()
                        # otherPlayer.save()

                        return JsonResponse({ 'InvestOrReturn':InvestOrReturn, 
                            'found': 1, 'returnAmount':returnAmount, 
                            'investAmount':investAmount, 'points':investment.points })
                    else:
                        if investment.otherreturned != -1:
                            return JsonResponse({ 'InvestOrReturn':True, 
                                'found': 1, 'returnAmount':investment.otherreturned, 
                                'investAmount':investment.invested, 'points':investment.points })
                        elif investment.otherinvested != -1:
                            investAmount = investment.otherinvested
                            if investAmount == 0:
                                returnAmount = investment.returned0
                            elif investAmount == 1:
                                returnAmount = investment.returned1
                            elif investAmount == 2:
                                returnAmount = investment.returned2
                            elif investAmount == 3:
                                returnAmount = investment.returned3
                            elif investAmount == 4:
                                returnAmount = investment.returned4
                            elif investAmount == 5:
                                returnAmount = investment.returned5
                            return JsonResponse({ 'InvestOrReturn':False, 'found': 1, 
                                'returnAmount':returnAmount, 
                                'investAmount':investAmount, 'points':investment.points })
                context = { 'umid': umid, 'gameNum':gameNum }
                return render(request, 'games/Trust Game.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

@ensure_csrf_cookie
def thankyou(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        user = User.objects.get(username=umid)
        holtLauryEarning = round(user.holtlaury_set.all()[0].points,2)
        gambleEarning = round(user.gamble_set.all()[0].points,2)
        investmentEarning = round(user.investment_set.all()[0].points,2)
        experimentEarning = round(holtLauryEarning + gambleEarning + investmentEarning,2)
        totalEarning = round(holtLauryEarning + gambleEarning + investmentEarning + 5,2)
        user.totalearning = round(totalEarning,2)
        user.experimentearning = round(experimentEarning,2)
        try:
            user.startedstudy = datetime.datetime.strptime(request.session['startedStudy'], '%b %d %Y %I:%M:%S %p')
        except:
            try:
                if user.pretest_set.count() != 0:
                    pretest = user.pretest_set.all()[0]
                    user.startedstudy = pretest.startedquestion1
                    print("\n\n\nTook started from the pretest.")
                else:
                    user.startedstudy = datetime.datetime.now()
                    print("\n\n\nTook started from now.")
            except:
                user.startedstudy = datetime.datetime.now()
                print("\n\n\nTook started from now in the except.")
        user.finishedstudy = datetime.datetime.now()
        user.optout = False
        user.postpone = False
        user.save()
        context = { 'umid': umid, 'holtLauryEarning': "%.2f" % holtLauryEarning, 'gambleEarning': gambleEarning, 
            'investmentEarning': "%.2f" % investmentEarning, 'experimentEarning': "%.2f" % experimentEarning, 
            'totalEarning': "%.2f" % totalEarning }
        return render(request, 'games/Thankyou.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def thankyousubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('fullnameInput' in request.POST and 
                'streetInput' in request.POST and 'cityInput' in request.POST and 
                'stateInput' in request.POST and 'zipcodeInput' in request.POST):
                fullnameInput = request.POST['fullnameInput']
                streetInput = request.POST['streetInput']
                cityInput = request.POST['cityInput']
                stateInput = request.POST['stateInput']
                zipcodeInput = request.POST['zipcodeInput']

                user = User.objects.get(username=umid)
                user.fullname = fullnameInput
                user.street = streetInput
                user.city = cityInput
                user.state = stateInput
                user.zipcode = zipcodeInput
                user.save()

                return JsonResponse({  })

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

@ensure_csrf_cookie
def survey(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        context = { 'umid': umid }
        return render(request, 'games/Survey.html', context)

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def convertNum2Bool(numObj):
    if numObj == 1 or numObj == "1" or numObj == "true" or numObj == "True":
        return True
    elif numObj == 0 or numObj == "0" or numObj == "false" or numObj == "False":
        return False

def surveysubmit(request):
    if request.method == 'POST':
        if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
            (request.session.get('umid', False) and request.session['umid'] != "")):
            if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                umid = request.META['REMOTE_USER']
            if (request.session.get('umid', False) and request.session['umid'] != ""):
                umid = request.session['umid']
            if ('emailsperday' in request.POST and 
                'PCLaptop' in request.POST and 'smartphone' in request.POST and 
                'PAD' in request.POST and 'otherDevices' in request.POST and 
                'yearsOfInternet' in request.POST and 'otherDeviceText' in request.POST):
                emailsperday = request.POST['emailsperday']
                PCLaptop = request.POST['PCLaptop']
                smartphone = request.POST['smartphone']
                PAD = request.POST['PAD']
                otherDevices = request.POST['otherDevices']
                otherDeviceText = request.POST['otherDeviceText']
                yearsOfInternet = request.POST['yearsOfInternet']

                user = User.objects.get(username=umid)
                user.emailsperday = emailsperday
                user.ownpc = convertNum2Bool(PCLaptop)
                user.ownsmartphone = convertNum2Bool(smartphone)
                user.ownpda = convertNum2Bool(PAD)
                user.ownotherdevice = convertNum2Bool(otherDevices)
                user.otherdevice = otherDeviceText
                user.internetuse = yearsOfInternet
                user.save()

                return JsonResponse({  })

    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def postpone(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        user = User.objects.get(username=umid)
        user.optout = False
        user.postpone = True
        user.save()
        context = { 'umid': umid, 'welcomepage': 1 }
        return render(request, 'games/Postpone.html', context)
    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def optout(request):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        user = User.objects.get(username=umid)
        user.optout = True
        user.postpone = False
        user.save()
        context = { 'umid': umid, 'welcomepage': 1 }
        return render(request, 'games/NotInterested.html', context)
    context = { 'umid': '', 'welcomepage': 1 }
    return render(request, 'games/Welcome.html', context)

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

def findStatistics(dataObj):
    dataObjMean = round(mean(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMin = round(min(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMax = round(max(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjStdev = round(pstdev(dataObj),3) if len(dataObj) > 1 else float('nan')
    dataObjMedian = round(median(dataObj),3) if len(dataObj) > 0 else float('nan')
    dataObjMode = round(max(set(dataObj), key=dataObj.count),3) if len(dataObj) > 0 else float('nan')

    return (dataObjMean, dataObjMin, dataObjMax, dataObjStdev, dataObjMedian, dataObjMode)

adminsUniquenames = ["yanchen", "oneweb", "arkzhang"]

def results(request):
    # try:
        if request.method == 'GET':
            if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
                (request.session.get('umid', False) and request.session['umid'] != "")):
                if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
                    umid = request.META['REMOTE_USER']
                if (request.session.get('umid', False) and request.session['umid'] != ""):
                    umid = request.session['umid']
                if (umid in adminsUniquenames):

                    version = "Pilot"
                    page = "Overview"
                    if ('version' in request.GET and request.GET['version'] != '' and request.GET['version'] != 'undefined'):
                        version = request.GET['version']
                    if ('page' in request.GET and request.GET['page'] != '' and request.GET['page'] != 'undefined'):
                        page = request.GET['page']

                    allUsers = User.objects.filter(version=version)
                    allUsers = list(allUsers)

                    questionCorrects = [[] for i in range(8)]
                    questionHovers = [[] for i in range(8)]
                    usersCorrects = []
                    usersHovers = []
                    usersDurations = []
                    totalCorrects = []
                    totalHovers = []
                    corrects = [0]*8
                    clicks = [0]*8
                    rightClicks = [0]*8
                    questionhovereds = [0]*8
                    hoveredsseconds = [[] for i in range(8)]
                    secondsDurations = [[] for i in range(8)]

                    userIndex = 0
                    allUsersLen = len(allUsers)
                    while userIndex < allUsersLen:
                        user = allUsers[userIndex]
                        pretest = user.pretest_set.all()
                        if len(pretest) > 0:
                            pretest = pretest[0]
                            usersCorrects.append(0)
                            usersHovers.append(0)
                            usersDurations.append(0)
                            userCorrect = [0]*8
                            userCorrect[1] = pretest.correct1
                            if userCorrect[1] == 2:
                                userCorrect[1] = 0
                            userCorrect[2] = pretest.correct2
                            if userCorrect[2] == 2:
                                userCorrect[2] = 0
                            userCorrect[3] = pretest.correct3
                            if userCorrect[3] == 2:
                                userCorrect[3] = 0
                            userCorrect[4] = pretest.correct4
                            if userCorrect[4] == 2:
                                userCorrect[4] = 0
                            userCorrect[5] = pretest.correct5
                            if userCorrect[5] == 2:
                                userCorrect[5] = 0
                            userCorrect[6] = pretest.correct6
                            if userCorrect[6] == 2:
                                userCorrect[6] = 0
                            userCorrect[7] = pretest.correct7
                            if userCorrect[7] == 2:
                                userCorrect[7] = 0
                            for index in range(1, 8):
                                corrects[index] += userCorrect[index]
                                usersCorrects[userIndex] += userCorrect[index]
                                questionCorrects[index].append(userCorrect[index])
                                totalCorrects.append(userCorrect[index])
                            rightClicks[1] += pretest.questionrightclicked1
                            rightClicks[2] += pretest.questionrightclicked2
                            rightClicks[3] += pretest.questionrightclicked3
                            rightClicks[4] += pretest.questionrightclicked4
                            rightClicks[5] += pretest.questionrightclicked5
                            rightClicks[6] += pretest.questionrightclicked6
                            rightClicks[7] += pretest.questionrightclicked7
                            questionhovereds[1] += pretest.questionhovered1
                            questionhovereds[2] += pretest.questionhovered2
                            questionhovereds[3] += pretest.questionhovered3
                            questionhovereds[4] += pretest.questionhovered4
                            questionhovereds[5] += pretest.questionhovered5
                            questionhovereds[6] += pretest.questionhovered6
                            questionhovereds[7] += pretest.questionhovered7

                            hoveredsseconds[1].append(pretest.questionhoveredseconds1)
                            questionHovers[1].append(pretest.questionhoveredseconds1)
                            usersHovers[userIndex] += pretest.questionhoveredseconds1
                            totalHovers.append(pretest.questionhoveredseconds1)

                            hoveredsseconds[2].append(pretest.questionhoveredseconds2)
                            questionHovers[2].append(pretest.questionhoveredseconds2)
                            usersHovers[userIndex] += pretest.questionhoveredseconds2
                            totalHovers.append(pretest.questionhoveredseconds2)

                            hoveredsseconds[3].append(pretest.questionhoveredseconds3)
                            questionHovers[3].append(pretest.questionhoveredseconds3)
                            usersHovers[userIndex] += pretest.questionhoveredseconds3
                            totalHovers.append(pretest.questionhoveredseconds3)

                            hoveredsseconds[4].append(pretest.questionhoveredseconds4)
                            questionHovers[4].append(pretest.questionhoveredseconds4)
                            usersHovers[userIndex] += pretest.questionhoveredseconds4
                            totalHovers.append(pretest.questionhoveredseconds4)

                            hoveredsseconds[5].append(pretest.questionhoveredseconds5)
                            questionHovers[5].append(pretest.questionhoveredseconds5)
                            usersHovers[userIndex] += pretest.questionhoveredseconds5
                            totalHovers.append(pretest.questionhoveredseconds5)

                            hoveredsseconds[6].append(pretest.questionhoveredseconds6)
                            questionHovers[6].append(pretest.questionhoveredseconds6)
                            usersHovers[userIndex] += pretest.questionhoveredseconds6
                            totalHovers.append(pretest.questionhoveredseconds6)

                            hoveredsseconds[7].append(pretest.questionhoveredseconds7)
                            questionHovers[7].append(pretest.questionhoveredseconds7)
                            usersHovers[userIndex] += pretest.questionhoveredseconds7
                            totalHovers.append(pretest.questionhoveredseconds7)

                            secondsDuration = [0]*8
                            secondsDuration[1] = pretest.finishedquestion1 - pretest.startedquestion1
                            secondsDuration[2] = pretest.finishedquestion2 - pretest.startedquestion2
                            secondsDuration[3] = pretest.finishedquestion3 - pretest.startedquestion3
                            secondsDuration[4] = pretest.finishedquestion4 - pretest.startedquestion4
                            secondsDuration[5] = pretest.finishedquestion5 - pretest.startedquestion5
                            secondsDuration[6] = pretest.finishedquestion6 - pretest.startedquestion6
                            secondsDuration[7] = pretest.finishedquestion7 - pretest.startedquestion7
                            for index in range(1, 8):
                                secondsDuration[index] = secondsDuration[index].total_seconds()
                                secondsDurations[index].append(secondsDuration[index])
                                usersDurations[userIndex] += secondsDuration[index]

                            userIndex += 1
                        else:
                            del allUsers[userIndex]
                            allUsersLen -= 1

                    usersCorrects = array(usersCorrects)
                    usersHovers = array(usersHovers)
                    usersDurations = array(usersDurations)

                    if page == "Overview":
                        experimentEarnings = []
                        minutesDurations = []

                        experimentEarningsTotal = 0

                        for user in allUsers:
                            experimentEarningsTotal += user.experimentearning
                            experimentEarnings.append(user.experimentearning)
                            timedeltaDuration = user.finishedstudy - user.startedstudy
                            secondsDuration = timedeltaDuration.total_seconds()
                            minutesDuration = secondsDuration // 60
                            minutesDurations.append(minutesDuration)

                        (experimentEarningsMean, experimentEarningsMin, experimentEarningsMax, 
                            experimentEarningsStdev, experimentEarningsMedian, 
                            experimentEarningsMode) = findStatistics(experimentEarnings)

                        (minutesDurationsMean, minutesDurationsMin, minutesDurationsMax, 
                            minutesDurationsStdev, minutesDurationsMedian, 
                            minutesDurationsMode) = findStatistics(minutesDurations)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'welcomepage': 1, 'page': page, 'version': version, 
                            'experimentEarningsMean': experimentEarningsMean, 'experimentEarningsTotal': round(experimentEarningsTotal,3), 
                            'experimentEarningsMin': experimentEarningsMin, 'experimentEarningsMax': experimentEarningsMax, 
                            'experimentEarningsStdev': experimentEarningsStdev, 'experimentEarningsMedian': experimentEarningsMedian, 
                            'experimentEarningsMode': experimentEarningsMode, 
                            'minutesDurations': minutesDurations, 'minutesDurationsMean': minutesDurationsMean, 
                            'minutesDurationsMin': minutesDurationsMin, 'minutesDurationsMax': minutesDurationsMax, 
                            'minutesDurationsStdev': minutesDurationsStdev, 'minutesDurationsMedian': minutesDurationsMedian, 
                            'minutesDurationsMode': minutesDurationsMode }

                    elif page == "Pretest":
                        hoveredssecondsMean = [0]*8
                        hoveredssecondsMin = [0]*8
                        hoveredssecondsMax = [0]*8
                        hoveredssecondsStdev = [0]*8
                        hoveredssecondsMedian = [0]*8
                        hoveredssecondsMode = [0]*8
                        for index in range(1, 8):
                            (hoveredssecondsMean[index], hoveredssecondsMin[index], hoveredssecondsMax[index], 
                                hoveredssecondsStdev[index], hoveredssecondsMedian[index], 
                                hoveredssecondsMode[index]) = findStatistics(hoveredsseconds[index])

                        secondsDurationsMean = [0]*8
                        secondsDurationsMin = [0]*8
                        secondsDurationsMax = [0]*8
                        secondsDurationsStdev = [0]*8
                        secondsDurationsMedian = [0]*8
                        secondsDurationsMode = [0]*8
                        for index in range(1, 8):
                            (secondsDurationsMean[index], secondsDurationsMin[index], secondsDurationsMax[index], 
                                secondsDurationsStdev[index], secondsDurationsMedian[index], 
                                secondsDurationsMode[index]) = findStatistics(secondsDurations[index])

                        usersHoversSlope, usersHoversIntercept, usersHoversR_value, usersHoversP_value, usersHoversStd_err = stats.linregress(usersHovers,usersCorrects[0:len(usersHovers)])

                        usersHoversSlope = round(usersHoversSlope,3)
                        usersHoversIntercept = round(usersHoversIntercept,3)
                        usersHoversR_value = round(usersHoversR_value,3)
                        usersHoversP_value = round(usersHoversP_value,3)
                        usersHoversStd_err = round(usersHoversStd_err,3)

                        usersDurationsSlope, usersDurationsIntercept, usersDurationsR_value, usersDurationsP_value, usersDurationsStd_err = stats.linregress(usersDurations,usersCorrects[0:len(usersDurations)])

                        usersDurationsSlope = round(usersDurationsSlope,3)
                        usersDurationsIntercept = round(usersDurationsIntercept,3)
                        usersDurationsR_value = round(usersDurationsR_value,3)
                        usersDurationsP_value = round(usersDurationsP_value,3)
                        usersDurationsStd_err = round(usersDurationsStd_err,3)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'page': page, 'version': version, 
                            'corrects': corrects, 'usersCorrects': usersCorrects, 
                            'clicks': clicks, 
                            'rightClicks': rightClicks, 
                            'questionhovereds': questionhovereds, 
                            'hoveredssecondsMean': hoveredssecondsMean, 
                            'hoveredssecondsMin': hoveredssecondsMin, 'hoveredssecondsMax': hoveredssecondsMax, 
                            'hoveredssecondsStdev': hoveredssecondsStdev, 'hoveredssecondsMedian': hoveredssecondsMedian, 
                            'hoveredssecondsMode': hoveredssecondsMode, 
                            'usersHovers': usersHovers, 'usersHoversSlope': usersHoversSlope, 
                            'usersHoversIntercept':usersHoversIntercept, 'usersHoversR_value': usersHoversR_value, 
                            'usersHoversP_value': usersHoversP_value, 'usersHoversStd_err': usersHoversStd_err,
                            'usersDurations': usersDurations, 'usersDurationsSlope': usersDurationsSlope, 
                            'usersDurationsIntercept':usersDurationsIntercept, 'usersDurationsR_value': usersDurationsR_value, 
                            'usersDurationsP_value': usersDurationsP_value, 'usersDurationsStd_err': usersDurationsStd_err,
                            'secondsDurations': secondsDurations, 'secondsDurationsMean': secondsDurationsMean, 
                            'secondsDurationsMin': secondsDurationsMin, 'secondsDurationsMax': secondsDurationsMax, 
                            'secondsDurationsStdev': secondsDurationsStdev, 'secondsDurationsMedian': secondsDurationsMedian, 
                            'secondsDurationsMode': secondsDurationsMode, 
                            }

                    elif page == "Lottery":
                        options = [0]*11
                        totalCorrectsPerOption = [0]*11
                        numOfCorrectsPerOption = [0]*11
                        totalPoints = 0
                        totalOriginalPoints = 0
                        totalWillingness = 0
                        points = []
                        originalPoints = []
                        willingness = []
                        secondsDurations = []
                        usersRiskAversion = []
                        usersWillingness = []
                        usersLotteryDurations = []

                        userIndex = 0
                        allUsersLen = len(allUsers)
                        while userIndex < allUsersLen:
                            user = allUsers[userIndex]
                            holtlaury = user.holtlaury_set.all()
                            if len(holtlaury) > 0:
                                holtlaury = holtlaury[0]
                                usersRiskAversion.append(0)
                                usersWillingness.append(0)
                                usersLotteryDurations.append(0)
                                option = [0]*11
                                option[1] = int(holtlaury.option1)
                                option[2] = int(holtlaury.option2)
                                option[3] = int(holtlaury.option3)
                                option[4] = int(holtlaury.option4)
                                option[5] = int(holtlaury.option5)
                                option[6] = int(holtlaury.option6)
                                option[7] = int(holtlaury.option7)
                                option[8] = int(holtlaury.option8)
                                option[9] = int(holtlaury.option9)
                                option[10] = int(holtlaury.option10)
                                rationalUser = True
                                if option[10] == 0:
                                    del allUsers[userIndex]
                                    usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                    del usersRiskAversion[userIndex]
                                    del usersWillingness[userIndex]
                                    del usersLotteryDurations[userIndex]
                                    rationalUser = False
                                    allUsersLen -= 1
                                    continue
                                for index in range(1, 11):
                                    if option[index] == 1 and usersRiskAversion[userIndex] == 0:
                                        usersRiskAversion[userIndex] = index
                                    elif option[index] == 0 and usersRiskAversion[userIndex] != 0:
                                        del allUsers[userIndex]
                                        usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                        del usersRiskAversion[userIndex]
                                        del usersWillingness[userIndex]
                                        del usersLotteryDurations[userIndex]
                                        rationalUser = False
                                        allUsersLen -= 1
                                        break
                                if rationalUser:
                                    for index in range(1, 11):
                                        options[index] += option[index]
                                        if option[index] != 0:
                                            totalCorrectsPerOption[index] += usersCorrects[userIndex]
                                            numOfCorrectsPerOption[index] += 1
                                    points.append(holtlaury.points)
                                    totalPoints += holtlaury.points
                                    originalPoints.append(holtlaury.originalPoints)
                                    totalOriginalPoints += holtlaury.originalPoints
                                    willingness.append(holtlaury.willingness)
                                    usersWillingness[userIndex] = holtlaury.willingness
                                    totalWillingness += holtlaury.willingness

                                    secondsDuration = holtlaury.finished - holtlaury.started
                                    secondsDuration = secondsDuration.total_seconds()
                                    secondsDurations.append(secondsDuration)
                                    usersLotteryDurations[userIndex] = secondsDuration

                                    userIndex += 1
                            else:
                                del allUsers[userIndex]
                                usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                allUsersLen -= 1

                        (pointsMean, pointsMin, pointsMax, 
                            pointsStdev, pointsMedian, 
                            pointsMode) = findStatistics(points)
                        (originalPointsMean, originalPointsMin, originalPointsMax, 
                            originalPointsStdev, originalPointsMedian, 
                            originalPointsMode) = findStatistics(originalPoints)
                        (willingnessMean, willingnessMin, willingnessMax, 
                            willingnessStdev, willingnessMedian, 
                            willingnessMode) = findStatistics(willingness)

                        (secondsDurationsMean, secondsDurationsMin, secondsDurationsMax, 
                            secondsDurationsStdev, secondsDurationsMedian, 
                            secondsDurationsMode) = findStatistics(secondsDurations)

                        usersRiskAversionSlope, usersRiskAversionIntercept, usersRiskAversionR_value, usersRiskAversionP_value, usersRiskAversionStd_err = stats.linregress(usersRiskAversion,usersCorrects)

                        usersRiskAversionSlope = round(usersRiskAversionSlope,3)
                        usersRiskAversionIntercept = round(usersRiskAversionIntercept,3)
                        usersRiskAversionR_value = round(usersRiskAversionR_value,3)
                        usersRiskAversionP_value = round(usersRiskAversionP_value,3)
                        usersRiskAversionStd_err = round(usersRiskAversionStd_err,3)

                        usersWillingnessSlope, usersWillingnessIntercept, usersWillingnessR_value, usersWillingnessP_value, usersWillingnessStd_err = stats.linregress(usersWillingness,usersCorrects)

                        usersWillingnessSlope = round(usersWillingnessSlope,3)
                        usersWillingnessIntercept = round(usersWillingnessIntercept,3)
                        usersWillingnessR_value = round(usersWillingnessR_value,3)
                        usersWillingnessP_value = round(usersWillingnessP_value,3)
                        usersWillingnessStd_err = round(usersWillingnessStd_err,3)

                        usersLotteryDurationsSlope, usersLotteryDurationsIntercept, usersLotteryDurationsR_value, usersLotteryDurationsP_value, usersLotteryDurationsStd_err = stats.linregress(usersLotteryDurations,usersCorrects)

                        usersLotteryDurationsSlope = round(usersLotteryDurationsSlope,3)
                        usersLotteryDurationsIntercept = round(usersLotteryDurationsIntercept,3)
                        usersLotteryDurationsR_value = round(usersLotteryDurationsR_value,3)
                        usersLotteryDurationsP_value = round(usersLotteryDurationsP_value,3)
                        usersLotteryDurationsStd_err = round(usersLotteryDurationsStd_err,3)

                        usersLotteryDurationsRiskAversionSlope, usersLotteryDurationsRiskAversionIntercept, usersLotteryDurationsRiskAversionR_value, usersLotteryDurationsRiskAversionP_value, usersLotteryDurationsRiskAversionStd_err = stats.linregress(usersLotteryDurations,usersRiskAversion)

                        usersLotteryDurationsRiskAversionSlope = round(usersLotteryDurationsRiskAversionSlope,3)
                        usersLotteryDurationsRiskAversionIntercept = round(usersLotteryDurationsRiskAversionIntercept,3)
                        usersLotteryDurationsRiskAversionR_value = round(usersLotteryDurationsRiskAversionR_value,3)
                        usersLotteryDurationsRiskAversionP_value = round(usersLotteryDurationsRiskAversionP_value,3)
                        usersLotteryDurationsRiskAversionStd_err = round(usersLotteryDurationsRiskAversionStd_err,3)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'page': page, 'version': version, 
                            'options': options, 'totalPoints': round(totalPoints,3), 'points': points, 'usersCorrects': usersCorrects, 
                            'totalCorrectsPerOption': totalCorrectsPerOption, 'numOfCorrectsPerOption': numOfCorrectsPerOption, 'pointsMean': pointsMean, 
                            'pointsMin': pointsMin, 'pointsMax': pointsMax, 
                            'pointsStdev': pointsStdev, 'pointsMedian': pointsMedian, 
                            'pointsMode': pointsMode, 
                            'originalPoints': originalPoints, 'totalOriginalPoints': round(totalOriginalPoints,3), 'originalPointsMean': originalPointsMean, 
                            'originalPointsMin': originalPointsMin, 'originalPointsMax': originalPointsMax, 
                            'originalPointsStdev': originalPointsStdev, 'originalPointsMedian': originalPointsMedian, 
                            'originalPointsMode': originalPointsMode, 
                            'willingness': willingness, 'totalWillingness': round(totalWillingness,3), 'willingnessMean': willingnessMean, 
                            'willingnessMin': willingnessMin, 'willingnessMax': willingnessMax, 
                            'willingnessStdev': willingnessStdev, 'willingnessMedian': willingnessMedian, 
                            'willingnessMode': willingnessMode, 
                            'secondsDurations': secondsDurations, 'secondsDurationsMean': secondsDurationsMean, 
                            'secondsDurationsMin': secondsDurationsMin, 'secondsDurationsMax': secondsDurationsMax, 
                            'secondsDurationsStdev': secondsDurationsStdev, 'secondsDurationsMedian': secondsDurationsMedian, 
                            'secondsDurationsMode': secondsDurationsMode, 
                            'usersRiskAversion': usersRiskAversion, 'usersRiskAversionSlope': usersRiskAversionSlope, 
                            'usersRiskAversionIntercept':usersRiskAversionIntercept, 'usersRiskAversionR_value': usersRiskAversionR_value, 
                            'usersRiskAversionP_value': usersRiskAversionP_value, 'usersRiskAversionStd_err': usersRiskAversionStd_err,
                            'usersWillingness': usersWillingness, 'usersWillingnessSlope': usersWillingnessSlope, 
                            'usersWillingnessIntercept':usersWillingnessIntercept, 'usersWillingnessR_value': usersWillingnessR_value, 
                            'usersWillingnessP_value': usersWillingnessP_value, 'usersWillingnessStd_err': usersWillingnessStd_err,
                            'usersLotteryDurations': usersLotteryDurations, 'usersLotteryDurationsSlope': usersLotteryDurationsSlope, 
                            'usersLotteryDurationsIntercept':usersLotteryDurationsIntercept, 'usersLotteryDurationsR_value': usersLotteryDurationsR_value, 
                            'usersLotteryDurationsP_value': usersLotteryDurationsP_value, 'usersLotteryDurationsStd_err': usersLotteryDurationsStd_err,
                            'usersLotteryDurationsRiskAversionSlope': usersLotteryDurationsRiskAversionSlope, 
                            'usersLotteryDurationsRiskAversionIntercept':usersLotteryDurationsRiskAversionIntercept, 'usersLotteryDurationsRiskAversionR_value': usersLotteryDurationsRiskAversionR_value, 
                            'usersLotteryDurationsRiskAversionP_value': usersLotteryDurationsRiskAversionP_value, 'usersLotteryDurationsRiskAversionStd_err': usersLotteryDurationsRiskAversionStd_err,
                            }

                    elif page == "Gamble":
                        usersRiskAversion = []
                        totalCorrectsPerOption = [0]*11
                        numOfCorrectsPerOption = [0]*11

                        chosens = []
                        points = []
                        secondsDurations = []
                        totalPoints = 0

                        userIndex = 0
                        allUsersLen = len(allUsers)
                        while userIndex < allUsersLen:
                            user = allUsers[userIndex]
                            holtlaury = user.holtlaury_set.all()
                            if len(holtlaury) > 0:
                                holtlaury = holtlaury[0]
                                usersRiskAversion.append(0)
                                option = [0]*11
                                option[1] = int(holtlaury.option1)
                                option[2] = int(holtlaury.option2)
                                option[3] = int(holtlaury.option3)
                                option[4] = int(holtlaury.option4)
                                option[5] = int(holtlaury.option5)
                                option[6] = int(holtlaury.option6)
                                option[7] = int(holtlaury.option7)
                                option[8] = int(holtlaury.option8)
                                option[9] = int(holtlaury.option9)
                                option[10] = int(holtlaury.option10)
                                rationalUser = True
                                if option[10] == 0:
                                    del allUsers[userIndex]
                                    usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                    del usersRiskAversion[userIndex]
                                    rationalUser = False
                                    allUsersLen -= 1
                                    continue
                                for index in range(1, 11):
                                    if option[index] == 1 and usersRiskAversion[userIndex] == 0:
                                        usersRiskAversion[userIndex] = index
                                    elif option[index] == 0 and usersRiskAversion[userIndex] != 0:
                                        del allUsers[userIndex]
                                        usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                        del usersRiskAversion[userIndex]
                                        rationalUser = False
                                        allUsersLen -= 1
                                        break
                                if rationalUser:
                                    gamble = user.gamble_set.all()
                                    if len(gamble) > 0:
                                        gamble = gamble[0]
                                        chosens.append(gamble.chosen)
                                        totalCorrectsPerOption[gamble.chosen] += usersCorrects[userIndex]
                                        numOfCorrectsPerOption[gamble.chosen] += 1
                                        points.append(gamble.points)
                                        totalPoints += gamble.points

                                        secondsDuration = gamble.finished - gamble.started
                                        secondsDuration = secondsDuration.total_seconds()
                                        secondsDurations.append(secondsDuration)

                                    userIndex += 1
                            else:
                                del allUsers[userIndex]
                                usersCorrects = numpy.delete(usersCorrects, [userIndex])
                                allUsersLen -= 1

                        (pointsMean, pointsMin, pointsMax, 
                            pointsStdev, pointsMedian, 
                            pointsMode) = findStatistics(points)

                        (chosensMean, chosensMin, chosensMax, 
                            chosensStdev, chosensMedian, 
                            chosensMode) = findStatistics(chosens)

                        (secondsDurationsMean, secondsDurationsMin, secondsDurationsMax, 
                            secondsDurationsStdev, secondsDurationsMedian, 
                            secondsDurationsMode) = findStatistics(secondsDurations)

                        usersRiskSeekingSlope, usersRiskSeekingIntercept, usersRiskSeekingR_value, usersRiskSeekingP_value, usersRiskSeekingStd_err = stats.linregress(chosens,usersCorrects[0:len(chosens)])

                        usersRiskSeekingSlope = round(usersRiskSeekingSlope,3)
                        usersRiskSeekingIntercept = round(usersRiskSeekingIntercept,3)
                        usersRiskSeekingR_value = round(usersRiskSeekingR_value,3)
                        usersRiskSeekingP_value = round(usersRiskSeekingP_value,3)
                        usersRiskSeekingStd_err = round(usersRiskSeekingStd_err,3)

                        usersRiskSeekingRiskAversionSlope, usersRiskSeekingRiskAversionIntercept, usersRiskSeekingRiskAversionR_value, usersRiskSeekingRiskAversionP_value, usersRiskSeekingRiskAversionStd_err = stats.linregress(chosens,usersRiskAversion[0:len(chosens)])

                        usersRiskSeekingRiskAversionSlope = round(usersRiskSeekingRiskAversionSlope,3)
                        usersRiskSeekingRiskAversionIntercept = round(usersRiskSeekingRiskAversionIntercept,3)
                        usersRiskSeekingRiskAversionR_value = round(usersRiskSeekingRiskAversionR_value,3)
                        usersRiskSeekingRiskAversionP_value = round(usersRiskSeekingRiskAversionP_value,3)
                        usersRiskSeekingRiskAversionStd_err = round(usersRiskSeekingRiskAversionStd_err,3)

                        usersGambleDurationsSlope, usersGambleDurationsIntercept, usersGambleDurationsR_value, usersGambleDurationsP_value, usersGambleDurationsStd_err = stats.linregress(secondsDurations,usersCorrects[0:len(secondsDurations)])

                        usersGambleDurationsSlope = round(usersGambleDurationsSlope,3)
                        usersGambleDurationsIntercept = round(usersGambleDurationsIntercept,3)
                        usersGambleDurationsR_value = round(usersGambleDurationsR_value,3)
                        usersGambleDurationsP_value = round(usersGambleDurationsP_value,3)
                        usersGambleDurationsStd_err = round(usersGambleDurationsStd_err,3)

                        usersGambleDurationsRiskSeekingSlope, usersGambleDurationsRiskSeekingIntercept, usersGambleDurationsRiskSeekingR_value, usersGambleDurationsRiskSeekingP_value, usersGambleDurationsRiskSeekingStd_err = stats.linregress(secondsDurations,chosens[0:len(secondsDurations)])

                        usersGambleDurationsRiskSeekingSlope = round(usersGambleDurationsRiskSeekingSlope,3)
                        usersGambleDurationsRiskSeekingIntercept = round(usersGambleDurationsRiskSeekingIntercept,3)
                        usersGambleDurationsRiskSeekingR_value = round(usersGambleDurationsRiskSeekingR_value,3)
                        usersGambleDurationsRiskSeekingP_value = round(usersGambleDurationsRiskSeekingP_value,3)
                        usersGambleDurationsRiskSeekingStd_err = round(usersGambleDurationsRiskSeekingStd_err,3)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'page': page, 'version': version, 
                            'totalPoints': round(totalPoints,3), 'points': points, 'usersCorrects': usersCorrects, 
                            'totalCorrectsPerOption': totalCorrectsPerOption, 'numOfCorrectsPerOption': numOfCorrectsPerOption, 'pointsMean': pointsMean, 
                            'pointsMin': pointsMin, 'pointsMax': pointsMax, 
                            'pointsStdev': pointsStdev, 'pointsMedian': pointsMedian, 
                            'pointsMode': pointsMode, 
                            'chosens': chosens, 'chosensMean': chosensMean, 
                            'chosensMin': chosensMin, 'chosensMax': chosensMax, 
                            'chosensStdev': chosensStdev, 'chosensMedian': chosensMedian, 
                            'chosensMode': chosensMode, 
                            'secondsDurations': secondsDurations, 'secondsDurationsMean': secondsDurationsMean, 
                            'secondsDurationsMin': secondsDurationsMin, 'secondsDurationsMax': secondsDurationsMax, 
                            'secondsDurationsStdev': secondsDurationsStdev, 'secondsDurationsMedian': secondsDurationsMedian, 
                            'secondsDurationsMode': secondsDurationsMode, 
                            'usersRiskSeekingSlope': usersRiskSeekingSlope, 
                            'usersRiskSeekingIntercept':usersRiskSeekingIntercept, 'usersRiskSeekingR_value': usersRiskSeekingR_value, 
                            'usersRiskSeekingP_value': usersRiskSeekingP_value, 'usersRiskSeekingStd_err': usersRiskSeekingStd_err,
                            'usersRiskAversion':usersRiskAversion, 'usersRiskSeekingRiskAversionSlope': usersRiskSeekingRiskAversionSlope, 
                            'usersRiskSeekingRiskAversionIntercept':usersRiskSeekingRiskAversionIntercept, 'usersRiskSeekingRiskAversionR_value': usersRiskSeekingRiskAversionR_value, 
                            'usersRiskSeekingRiskAversionP_value': usersRiskSeekingRiskAversionP_value, 'usersRiskSeekingRiskAversionStd_err': usersRiskSeekingRiskAversionStd_err,
                            'usersGambleDurationsSlope': usersGambleDurationsSlope, 
                            'usersGambleDurationsIntercept':usersGambleDurationsIntercept, 'usersGambleDurationsR_value': usersGambleDurationsR_value, 
                            'usersGambleDurationsP_value': usersGambleDurationsP_value, 'usersGambleDurationsStd_err': usersGambleDurationsStd_err,
                            'usersGambleDurationsRiskSeekingSlope': usersGambleDurationsRiskSeekingSlope, 
                            'usersGambleDurationsRiskSeekingIntercept':usersGambleDurationsRiskSeekingIntercept, 'usersGambleDurationsRiskSeekingR_value': usersGambleDurationsRiskSeekingR_value, 
                            'usersGambleDurationsRiskSeekingP_value': usersGambleDurationsRiskSeekingP_value, 'usersGambleDurationsRiskSeekingStd_err': usersGambleDurationsRiskSeekingStd_err,
                            }

                    elif page == "Investment":
                        invested = []
                        returned = [[] for i in range(6)]
                        points = []
                        totalPoints = 0
                        secondsInvestedDurations = []
                        secondsReturnedDurations = [[] for i in range(6)]

                        for user in allUsers:
                            investment = user.investment_set.all()
                            if len(investment) > 0:
                                investment = investment[0]
                                invested.append(investment.invested)
                                returned[0].append(investment.returned0)
                                returned[1].append(investment.returned1)
                                returned[2].append(investment.returned2)
                                returned[3].append(investment.returned3)
                                returned[4].append(investment.returned4)
                                returned[5].append(investment.returned5)
                                points.append(investment.points)
                                totalPoints += investment.points

                                secondsInvestedDuration = investment.finishedinvested - investment.startedinvested
                                secondsInvestedDuration = secondsInvestedDuration.total_seconds()
                                secondsInvestedDurations.append(secondsInvestedDuration)
                                secondsReturnedDuration = [0]*6
                                secondsReturnedDuration[0] = investment.finishedreturned0 - investment.startedreturned0
                                secondsReturnedDuration[1] = investment.finishedreturned1 - investment.startedreturned1
                                secondsReturnedDuration[2] = investment.finishedreturned2 - investment.startedreturned2
                                secondsReturnedDuration[3] = investment.finishedreturned3 - investment.startedreturned3
                                secondsReturnedDuration[4] = investment.finishedreturned4 - investment.startedreturned4
                                secondsReturnedDuration[5] = investment.finishedreturned5 - investment.startedreturned5
                                for index in range(0, 6):
                                    secondsReturnedDuration[index] = secondsReturnedDuration[index].total_seconds()
                                    secondsReturnedDurations[index].append(secondsReturnedDuration[index])

                        (investedMean, investedMin, investedMax, 
                            investedStdev, investedMedian, 
                            investedMode) = findStatistics(invested)

                        returnedMean = [0]*6
                        returnedMin = [0]*6
                        returnedMax = [0]*6
                        returnedStdev = [0]*6
                        returnedMedian = [0]*6
                        returnedMode = [0]*6
                        for index in range(0, 6):
                            (returnedMean[index], returnedMin[index], returnedMax[index], 
                                returnedStdev[index], returnedMedian[index], 
                                returnedMode[index]) = findStatistics(returned[index])

                        (pointsMean, pointsMin, pointsMax, 
                            pointsStdev, pointsMedian, 
                            pointsMode) = findStatistics(points)

                        (secondsInvestedDurationsMean, secondsInvestedDurationsMin, secondsInvestedDurationsMax, 
                            secondsInvestedDurationsStdev, secondsInvestedDurationsMedian, 
                            secondsInvestedDurationsMode) = findStatistics(secondsInvestedDurations)

                        secondsReturnedDurationsMean = [0]*6
                        secondsReturnedDurationsMin = [0]*6
                        secondsReturnedDurationsMax = [0]*6
                        secondsReturnedDurationsStdev = [0]*6
                        secondsReturnedDurationsMedian = [0]*6
                        secondsReturnedDurationsMode = [0]*6
                        for index in range(0, 6):
                            (secondsReturnedDurationsMean[index], secondsReturnedDurationsMin[index], secondsReturnedDurationsMax[index], 
                                secondsReturnedDurationsStdev[index], secondsReturnedDurationsMedian[index], 
                                secondsReturnedDurationsMode[index]) = findStatistics(secondsReturnedDurations[index])

                        usersTrustInvestmentSlope, usersTrustInvestmentIntercept, usersTrustInvestmentR_value, usersTrustInvestmentP_value, usersTrustInvestmentStd_err = stats.linregress(invested, usersCorrects[0:len(invested)])

                        usersTrustInvestmentSlope = round(usersTrustInvestmentSlope,3)
                        usersTrustInvestmentIntercept = round(usersTrustInvestmentIntercept,3)
                        usersTrustInvestmentR_value = round(usersTrustInvestmentR_value,3)
                        usersTrustInvestmentP_value = round(usersTrustInvestmentP_value,3)
                        usersTrustInvestmentStd_err = round(usersTrustInvestmentStd_err,3)

                        usersInvestmentDurationsSlope, usersInvestmentDurationsIntercept, usersInvestmentDurationsR_value, usersInvestmentDurationsP_value, usersInvestmentDurationsStd_err = stats.linregress(secondsInvestedDurations, invested[0:len(secondsInvestedDurations)])

                        usersInvestmentDurationsSlope = round(usersInvestmentDurationsSlope,3)
                        usersInvestmentDurationsIntercept = round(usersInvestmentDurationsIntercept,3)
                        usersInvestmentDurationsR_value = round(usersInvestmentDurationsR_value,3)
                        usersInvestmentDurationsP_value = round(usersInvestmentDurationsP_value,3)
                        usersInvestmentDurationsStd_err = round(usersInvestmentDurationsStd_err,3)

                        usersTrustreturnedSlope = [0]*6
                        usersTrustreturnedIntercept = [0]*6
                        usersTrustreturnedR_value = [0]*6
                        usersTrustreturnedP_value = [0]*6
                        usersTrustreturnedStd_err = [0]*6
                        for index in range(0, 6):
                            usersTrustreturnedSlope[index], usersTrustreturnedIntercept[index], usersTrustreturnedR_value[index], usersTrustreturnedP_value[index], usersTrustreturnedStd_err[index] = stats.linregress(returned[index], usersCorrects[0:len(returned[index])])

                            usersTrustreturnedSlope[index] = round(usersTrustreturnedSlope[index],3)
                            usersTrustreturnedIntercept[index] = round(usersTrustreturnedIntercept[index],3)
                            usersTrustreturnedR_value[index] = round(usersTrustreturnedR_value[index],3)
                            usersTrustreturnedP_value[index] = round(usersTrustreturnedP_value[index],3)
                            usersTrustreturnedStd_err[index] = round(usersTrustreturnedStd_err[index],3)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'page': page, 'version': version, 'usersCorrects': usersCorrects, 
                            'invested': invested, 'investedMean': investedMean, 
                            'investedMin': investedMin, 'investedMax': investedMax, 
                            'investedStdev': investedStdev, 'investedMedian': investedMedian, 
                            'investedMode': investedMode, 
                            'returned': returned, 'returnedMean': returnedMean, 
                            'returnedMin': returnedMin, 'returnedMax': returnedMax, 
                            'returnedStdev': returnedStdev, 'returnedMedian': returnedMedian, 
                            'returnedMode': returnedMode, 
                            'totalPoints': round(totalPoints,3), 'points': points, 'pointsMean': pointsMean, 
                            'pointsMin': pointsMin, 'pointsMax': pointsMax, 
                            'pointsStdev': pointsStdev, 'pointsMedian': pointsMedian, 
                            'pointsMode': pointsMode, 
                            'secondsInvestedDurations': secondsInvestedDurations, 'secondsInvestedDurationsMean': secondsInvestedDurationsMean, 
                            'secondsInvestedDurationsMin': secondsInvestedDurationsMin, 'secondsInvestedDurationsMax': secondsInvestedDurationsMax, 
                            'secondsInvestedDurationsStdev': secondsInvestedDurationsStdev, 'secondsInvestedDurationsMedian': secondsInvestedDurationsMedian, 
                            'secondsInvestedDurationsMode': secondsInvestedDurationsMode, 
                            'secondsReturnedDurationsMean': secondsReturnedDurationsMean, 
                            'secondsReturnedDurationsMin': secondsReturnedDurationsMin, 'secondsReturnedDurationsMax': secondsReturnedDurationsMax, 
                            'secondsReturnedDurationsStdev': secondsReturnedDurationsStdev, 'secondsReturnedDurationsMedian': secondsReturnedDurationsMedian, 
                            'secondsReturnedDurationsMode': secondsReturnedDurationsMode, 
                            'usersTrustInvestmentSlope': usersTrustInvestmentSlope, 
                            'usersTrustInvestmentIntercept':usersTrustInvestmentIntercept, 'usersTrustInvestmentR_value': usersTrustInvestmentR_value, 
                            'usersTrustInvestmentP_value': usersTrustInvestmentP_value, 'usersTrustInvestmentStd_err': usersTrustInvestmentStd_err,
                            'usersInvestmentDurationsSlope': usersInvestmentDurationsSlope, 
                            'usersInvestmentDurationsIntercept':usersInvestmentDurationsIntercept, 'usersInvestmentDurationsR_value': usersInvestmentDurationsR_value, 
                            'usersInvestmentDurationsP_value': usersInvestmentDurationsP_value, 'usersInvestmentDurationsStd_err': usersInvestmentDurationsStd_err,
                            'usersTrustreturnedSlope': usersTrustreturnedSlope,
                            'usersTrustreturnedIntercept': usersTrustreturnedIntercept,
                            'usersTrustreturnedR_value': usersTrustreturnedR_value,
                            'usersTrustreturnedP_value': usersTrustreturnedP_value,
                            'usersTrustreturnedStd_err': usersTrustreturnedStd_err,
                            }

                    elif page == "Comments":
                        comments = []

                        for user in allUsers:
                            userComments = user.thankyou_set.all()
                            if len(userComments) > 0:
                                userComments = userComments[0]
                                userComment = []
                                userComment.append(str(userComments.user))
                                userComment.append(userComments.pretestComment)
                                userComment.append(userComments.trainingComment)
                                userComment.append(userComments.gamesComment)
                                comments.append(userComment)

                        context = { 'umid': umid, 'allUsers': allUsers, 'welcomepage': 1, 'page': page, 'version': version, 
                            'comments': comments, 
                            }


                    return render(request, 'games/Results.html', context)

        context = { 'umid': '', 'welcomepage': 1 }
        return render(request, 'games/Welcome.html', context)
    # except:
    #     context = { 'umid': '', 'welcomepage': 1 }
    #     return render(request, 'games/Welcome.html', context)

class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def downloadCSV(request, experiment = "", part = ""):
    if (('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != "") or 
        (request.session.get('umid', False) and request.session['umid'] != "")):
        """A view that streams a large CSV file."""
        # Generate a sequence of rows. The range is based on the maximum number of
        # rows that can be handled by a single sheet in most spreadsheet
        # applications.
        if ('REMOTE_USER' in request.META and request.META['REMOTE_USER'] != ""):
            umid = request.META['REMOTE_USER']
        if (request.session.get('umid', False) and request.session['umid'] != ""):
            umid = request.session['umid']
        if (umid in adminsUniquenames):
            rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)

            print ("Experiment = " + experiment)

            rows = generateCSVDataset(experiment, part)

            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="PhishingDataset.csv"'
            return response

        context = { 'umid': '', 'welcomepage': 1 }
        return render(request, 'games/Welcome.html', context)

def generateCSVDataset(experiment, part):
    rows = []
    if experiment == "":
        rows.append(['Username', 'version', 'Experiment Earning', 
            'First Game', 'Second Game', 'Third Game', 'Opted Out', 'Postponed', 
            'age', 'gender', 'emailsperday', 'ownpc', 'ownsmartphone', 'owntablet', 
            'ownotherdevice', 'otherdevice', 'internetuse', 
            'fullname', 'street', 'city', 'state', 'zipcode', 'yearsofeduction', 'ethnicity', 
            'maritalstatus', 'Started Study', 'finishedstudy', 
            'Pretest Question 1', 'Pretest Question 2', 
            'Pretest Question 3', 'Pretest Question 4', 
            'Pretest Question 5', 'Pretest Question 6', 
            'Pretest Question 7', 
            'Pretest 1 Answer was Correct (1) / Wrong (2)', 'Pretest 2 Answer was Correct (1) / Wrong (2)', 
            'Pretest 3 Answer was Correct (1) / Wrong (2)', 'Pretest 4 Answer was Correct (1) / Wrong (2)', 
            'Pretest 5 Answer was Correct (1) / Wrong (2)', 'Pretest 6 Answer was Correct (1) / Wrong (2)', 
            'Pretest 7 Answer was Correct (1) / Wrong (2)', 
            'Pretest Question Clicked 1', 'Pretest Question Clicked 2', 
            'Pretest Question Clicked 3', 'Pretest Question Clicked 4', 
            'Pretest Question Clicked 5', 'Pretest Question Clicked 6', 
            'Pretest Question Clicked 7', 
            'Pretest Question Right Clicked 1', 'Pretest Question Right Clicked 2', 
            'Pretest Question Right Clicked 3', 'Pretest Question Right Clicked 4', 
            'Pretest Question Right Clicked 5', 'Pretest Question Right Clicked 6', 
            'Pretest Question Right Clicked 7', 
            'Pretest Question Hovered 1', 'Pretest Question Hovered 2', 
            'Pretest Question Hovered 3', 'Pretest Question Hovered 4', 
            'Pretest Question Hovered 5', 'Pretest Question Hovered 6', 
            'Pretest Question Hovered 7', 
            'Pretest Question Hovered Duration in Seconds 1', 'Pretest Question Hovered Duration in Seconds 2', 
            'Pretest Question Hovered Duration in Seconds 3', 'Pretest Question Hovered Duration in Seconds 4', 
            'Pretest Question Hovered Duration in Seconds 5', 'Pretest Question Hovered Duration in Seconds 6', 
            'Pretest Question Hovered Duration in Seconds 7', 
            'Pretest Started Question 1', 'Pretest Finished Question 1', 
            'Pretest Started Question 2', 'Pretest Finished Question 2', 
            'Pretest Started Question 3', 'Pretest Finished Question 3', 
            'Pretest Started Question 4', 'Pretest Finished Question 4', 
            'Pretest Started Question 5', 'Pretest Finished Question 5', 
            'Pretest Started Question 6', 'Pretest Finished Question 6', 
            'Pretest Started Question 7', 'Pretest Finished Question 7', 
            'Training Question 1', 'Training Question 2', 
            'Training Question 3', 
            'Training 1 Answer was Correct (1) / Wrong (2)', 'Training 2 Answer was Correct (1) / Wrong (2)', 
            'Training 3 Answer was Correct (1) / Wrong (2)', 
            'Training Question Clicked 1', 'Training Question Clicked 2', 
            'Training Question Clicked 3', 
            'Training Question Right Clicked 1', 'Training Question Right Clicked 2', 
            'Training Question Right Clicked 3', 
            'Training Question Hovered 1', 'Training Question Hovered 2', 
            'Training Question Hovered 3', 
            'Training Question Hovered Duration in Seconds 1', 'Training Question Hovered Duration in Seconds 2', 
            'Training Question Hovered Duration in Seconds 3', 
            'Training Started Question 1', 'Training Finished Question 1', 
            'Training Started Question 2', 'Training Finished Question 2', 
            'Training Started Question 3', 'Training Finished Question 3', 
            'Lottery Decision', 'Lottery Option1', 'Lottery Option2',
            'Lottery Option3', 'Lottery Option4', 'Lottery Option5', 'Lottery Option6', 'Lottery Option7',
            'Lottery Option8', 'Lottery Option9', 'Lottery Option10', 'Lottery Die1', 'Lottery Die2',
            'Lottery Die3', 'Lottery Die4', 'Lottery Die5', 'Lottery Die6', 'Lottery Die7', 'Lottery Die8',
            'Lottery Die9', 'Lottery Die10', 'Lottery Original Points', 'Lottery Points',
            "Lottery Subject's Willingness", 'Lottery Random Willingness', 'Lottery Started',
            'Lottery Finished', 
            'Gamble Chosen', 'Gamble Coin 1', 'Gamble Coin 2',
            'Gamble Coin 3', 'Gamble Coin 4', 'Gamble Coin 5', 'Gamble Coin 6', 'Gamble Coin 7',
            'Gamble Coin 8', 'Gamble Coin 9', 'Gamble Points Earned',
            "Gamble Subject's Willingness", 'Gamble Random Willingness', 'Gamble Started',
            'Gamble Finished', 
            'Trust Game Invested', 'Trust Game Returned 0', 'Trust Game Returned 1', 'Trust Game Returned 2',
            'Trust Game Returned 3', 'Trust Game Returned 4', 'Trust Game Returned 5', 'Trust Game Played With',
            'Trust Game Other Player Returned', 'Trust Game Other Player Invested', 'Trust Game Points Earned', 
            'Trust Game Started Investment', 'Trust Game Finished Investment', 
            'Trust Game Started Return 0', 'Trust Game Finished Return 0', 
            'Trust Game Started Return 1', 'Trust Game Finished Return 1', 
            'Trust Game Started Return 2', 'Trust Game Finished Return 2', 
            'Trust Game Started Return 3', 'Trust Game Finished Return 3', 
            'Trust Game Started Return 4', 'Trust Game Finished Return 4', 
            'Trust Game Started Return 5', 'Trust Game Finished Return 5', 
            'Survey Pretest Comment', 'Survey Training Comment', 'Survey Games Comment',
            ])

        allUsers = User.objects.all()

        for user in allUsers:
            row = []
            row.append(user.username)
            row.append(user.version)
            row.append(user.experimentearning)
            row.append(user.firstgame)
            row.append(user.secondgame)
            row.append(user.thirdgame)
            row.append(user.optout)
            row.append(user.postpone)
            row.append(user.age)
            row.append(user.gender)
            row.append(user.emailsperday)
            row.append(user.ownpc)
            row.append(user.ownsmartphone)
            row.append(user.ownpda)
            row.append(user.ownotherdevice)
            row.append(user.otherdevice)
            row.append(user.internetuse)
            row.append(user.fullname)
            row.append(user.street)
            row.append(user.city)
            row.append(user.state)
            row.append(user.zipcode)
            row.append(user.yearsofeduction)
            row.append(user.ethnicity)
            row.append(user.maritalstatus)
            row.append(user.startedstudy)
            row.append(user.finishedstudy)

            if user.pretest_set.count() != 0:
                pretest = user.pretest_set.all()[0]
                row.append(pretest.question1)
                row.append(pretest.question2)
                row.append(pretest.question3)
                row.append(pretest.question4)
                row.append(pretest.question5)
                row.append(pretest.question6)
                row.append(pretest.question7)
                row.append(pretest.correct1)
                row.append(pretest.correct2)
                row.append(pretest.correct3)
                row.append(pretest.correct4)
                row.append(pretest.correct5)
                row.append(pretest.correct6)
                row.append(pretest.correct7)
                row.append(pretest.questionclicked1)
                row.append(pretest.questionclicked2)
                row.append(pretest.questionclicked3)
                row.append(pretest.questionclicked4)
                row.append(pretest.questionclicked5)
                row.append(pretest.questionclicked6)
                row.append(pretest.questionclicked7)
                row.append(pretest.questionrightclicked1)
                row.append(pretest.questionrightclicked2)
                row.append(pretest.questionrightclicked3)
                row.append(pretest.questionrightclicked4)
                row.append(pretest.questionrightclicked5)
                row.append(pretest.questionrightclicked6)
                row.append(pretest.questionrightclicked7)
                row.append(pretest.questionhovered1)
                row.append(pretest.questionhovered2)
                row.append(pretest.questionhovered3)
                row.append(pretest.questionhovered4)
                row.append(pretest.questionhovered5)
                row.append(pretest.questionhovered6)
                row.append(pretest.questionhovered7)
                row.append(pretest.questionhoveredseconds1)
                row.append(pretest.questionhoveredseconds2)
                row.append(pretest.questionhoveredseconds3)
                row.append(pretest.questionhoveredseconds4)
                row.append(pretest.questionhoveredseconds5)
                row.append(pretest.questionhoveredseconds6)
                row.append(pretest.questionhoveredseconds7)
                row.append(pretest.startedquestion1)
                row.append(pretest.finishedquestion1)
                row.append(pretest.startedquestion2)
                row.append(pretest.finishedquestion2)
                row.append(pretest.startedquestion3)
                row.append(pretest.finishedquestion3)
                row.append(pretest.startedquestion4)
                row.append(pretest.finishedquestion4)
                row.append(pretest.startedquestion5)
                row.append(pretest.finishedquestion5)
                row.append(pretest.startedquestion6)
                row.append(pretest.finishedquestion6)
                row.append(pretest.startedquestion7)
                row.append(pretest.finishedquestion7)
            else:
                for index in range(56):
                    row.append("")

            if user.training_set.count() != 0:
                training = user.training_set.all()[0]
                row.append(training.question1)
                row.append(training.question2)
                row.append(training.question3)
                row.append(training.correct1)
                row.append(training.correct2)
                row.append(training.correct3)
                row.append(training.questionclicked1)
                row.append(training.questionclicked2)
                row.append(training.questionclicked3)
                row.append(training.questionrightclicked1)
                row.append(training.questionrightclicked2)
                row.append(training.questionrightclicked3)
                row.append(training.questionhovered1)
                row.append(training.questionhovered2)
                row.append(training.questionhovered3)
                row.append(training.questionhoveredseconds1)
                row.append(training.questionhoveredseconds2)
                row.append(training.questionhoveredseconds3)
                row.append(training.startedquestion1)
                row.append(training.finishedquestion1)
                row.append(training.startedquestion2)
                row.append(training.finishedquestion2)
                row.append(training.startedquestion3)
                row.append(training.finishedquestion3)
            else:
                for index in range(24):
                    row.append("")

            if user.holtlaury_set.count() != 0:
                holtLaury = user.holtlaury_set.all()[0]
                row.append(holtLaury.decision)
                row.append(holtLaury.option1)
                row.append(holtLaury.option2)
                row.append(holtLaury.option3)
                row.append(holtLaury.option4)
                row.append(holtLaury.option5)
                row.append(holtLaury.option6)
                row.append(holtLaury.option7)
                row.append(holtLaury.option8)
                row.append(holtLaury.option9)
                row.append(holtLaury.option10)
                row.append(holtLaury.die1)
                row.append(holtLaury.die2)
                row.append(holtLaury.die3)
                row.append(holtLaury.die4)
                row.append(holtLaury.die5)
                row.append(holtLaury.die6)
                row.append(holtLaury.die7)
                row.append(holtLaury.die8)
                row.append(holtLaury.die9)
                row.append(holtLaury.die10)
                row.append(holtLaury.originalPoints)
                row.append(holtLaury.points)
                row.append(holtLaury.willingness)
                row.append(holtLaury.willingnessRand)
                row.append(holtLaury.started)
                row.append(holtLaury.finished)
            else:
                for index in range(27):
                    row.append("")

            if user.gamble_set.count() != 0:
                gamble = user.gamble_set.all()[0]
                row.append(gamble.chosen)
                row.append(gamble.coin1)
                row.append(gamble.coin2)
                row.append(gamble.coin3)
                row.append(gamble.coin4)
                row.append(gamble.coin5)
                row.append(gamble.coin6)
                row.append(gamble.coin7)
                row.append(gamble.coin8)
                row.append(gamble.coin9)
                row.append(gamble.points)
                row.append(gamble.willingness)
                row.append(gamble.willingnessRand)
                row.append(gamble.started)
                row.append(gamble.finished)
            else:
                for index in range(15):
                    row.append("")

            if user.investment_set.count() != 0:
                investment = user.investment_set.all()[0]
                row.append(investment.invested)
                row.append(investment.returned0)
                row.append(investment.returned1)
                row.append(investment.returned2)
                row.append(investment.returned3)
                row.append(investment.returned4)
                row.append(investment.returned5)
                row.append(investment.otheruser)
                row.append(investment.otherreturned)
                row.append(investment.otherinvested)
                row.append(investment.points)
                row.append(investment.startedinvested)
                row.append(investment.finishedinvested)
                row.append(investment.startedreturned0)
                row.append(investment.finishedreturned0)
                row.append(investment.startedreturned1)
                row.append(investment.finishedreturned1)
                row.append(investment.startedreturned2)
                row.append(investment.finishedreturned2)
                row.append(investment.startedreturned3)
                row.append(investment.finishedreturned3)
                row.append(investment.startedreturned4)
                row.append(investment.finishedreturned4)
                row.append(investment.startedreturned5)
                row.append(investment.finishedreturned5)
            else:
                for index in range(25):
                    row.append("")

            if user.thankyou_set.count() != 0:
                thankyou = user.thankyou_set.all()[0]
                row.append(thankyou.trainingComment)
                row.append(thankyou.gamesComment)
                row.append(thankyou.pretestComment)
            else:
                for index in range(3):
                    row.append("")

            rows.append(row)

    elif experiment == "Pilot":
        rows.append(['Username', 
            'Trust Game Invested', 'Trust Game Returned 0', 'Trust Game Returned 1', 'Trust Game Returned 2',
            'Trust Game Returned 3', 'Trust Game Returned 4', 'Trust Game Returned 5', 'Trust Game Played With',
            'Trust Game Other Player Returned', 'Trust Game Other Player Invested', 'Trust Game Points Earned', 
            'Trust Game Started Investment', 'Trust Game Finished Investment', 
            'Trust Game Started Return 0', 'Trust Game Finished Return 0', 
            'Trust Game Started Return 1', 'Trust Game Finished Return 1', 
            'Trust Game Started Return 2', 'Trust Game Finished Return 2', 
            'Trust Game Started Return 3', 'Trust Game Finished Return 3', 
            'Trust Game Started Return 4', 'Trust Game Finished Return 4', 
            'Trust Game Started Return 5', 'Trust Game Finished Return 5', 
            ])

        allUsers = User.objects.filter(version = 'Pilot')

        for user in allUsers:
            row = []
            row.append(user.username)

            if user.investment_set.count() != 0:
                investment = user.investment_set.all()[0]
                row.append(investment.invested)
                row.append(investment.returned0)
                row.append(investment.returned1)
                row.append(investment.returned2)
                row.append(investment.returned3)
                row.append(investment.returned4)
                row.append(investment.returned5)
                row.append(investment.otheruser)
                row.append(investment.otherreturned)
                row.append(investment.otherinvested)
                row.append(investment.points)
                row.append(investment.startedinvested)
                row.append(investment.finishedinvested)
                row.append(investment.startedreturned0)
                row.append(investment.finishedreturned0)
                row.append(investment.startedreturned1)
                row.append(investment.finishedreturned1)
                row.append(investment.startedreturned2)
                row.append(investment.finishedreturned2)
                row.append(investment.startedreturned3)
                row.append(investment.finishedreturned3)
                row.append(investment.startedreturned4)
                row.append(investment.finishedreturned4)
                row.append(investment.startedreturned5)
                row.append(investment.finishedreturned5)
            else:
                for index in range(25):
                    row.append("")

            rows.append(row)

    return rows
