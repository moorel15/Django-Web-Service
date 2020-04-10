from django.shortcuts import render
from django.core import serializers
from decimal import *
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json
from .models import Professor, Module, Student, Rating

@csrf_exempt
#register function
def register(request):
#check post request
    if request.method == 'POST':
    #get details of post request
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        #get all students and loop through until student found if not found register else tell the client what is already taken.
        allStudents = Student.objects.all().values('username', 'email')
        usernameUsed = False
        emailUsed = False
        for student in allStudents:
            if username == student['username']:
                usernameUsed = True
                break
            elif email == student['email']:
                emailUsed = True
                break
        if usernameUsed:
            return HttpResponse('Username')
        elif emailUsed:
            return HttpResponse('Email')
        else:
            i = Student.objects.create(name=name, username=username, email=email, password=password)
            return HttpResponse('OK')

@csrf_exempt
#login function
def login(request):
#check post request
    if request.method == 'POST':
    #get details of post
        username = request.POST.get('username')
        password = request.POST.get('password')
        #get all students, loop through until username and password match then tell client user found, can log in. else say no match cant log in.
        allStudents = Student.objects.all().values('username', 'password')
        userFound = False
        for student in allStudents:
            if student['username'] == str(username):
                if student['password'] == str(password):
                    userFound = True
                    break
        if userFound:
            return HttpResponse('OK')
        else:
            return HttpResponse('No Match')

@csrf_exempt
def allModules(request):
#check get request
    if request.method == 'GET':
    #get all modules and get the teachers from professors table, then load into list and send back to client.
        allModules = Module.objects.all().values('id', 'code', 'name', 'year', 'semester', 'taughtBy')
        listOfModules = []
        for module in allModules:
            m = Module.objects.get(id=module['id'])
            ps = m.taughtBy.all().values('name')
            names = ""
            for p in ps:
                name = str(p['name'])
                names += (name + ", ")
            i = {'code': module['code'] , 'name': module['name'] , 'year': module['year'] , 'semester': module['semester'] , 'taughtBy': names}
            duplicateFound = 0
            for ind, module in enumerate(listOfModules):
                if i == listOfModules[ind]:
                    duplicateFound = 1
            if duplicateFound == 0:
                listOfModules.append(i)
        pl = {'listOfModules' : listOfModules}
        http = HttpResponse(json.dumps(pl))
        http['Content-Type'] = 'application/json'
        http.status_code = 200
        http.reason_phrase = 'OK'
        return http
    else:
    #if wrong request tell client
        http = HttpResponseBadRequest()
        http['Content-Type'] = 'text/plain'
        http.content = "Bad Request, only get allowed."
        return http

@csrf_exempt
#average ratings function
def viewRatings(request):
#check get request
    if request.method == 'GET':
    #get all professors
        allProfs = Professor.objects.all().values('id', 'name', 'code')
        listOfAverages = []
        #for each professor, calculate average add the professor details to list and send to client
        for prof in allProfs:
            counter = 0
            total = 0
            ratingsOfProf = Rating.objects.all().filter(professor=prof['id']).values('rating')
            for rating in ratingsOfProf:
                counter += 1
                total += int(rating['rating'])
            average = Decimal(total/counter).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
            i = {'code' : prof['code'], 'name' : prof['name'], 'average' : str(average)}
            duplicateFound = 0
            for ind, module in enumerate(listOfAverages):
                if i == listOfAverages[ind]:
                    duplicateFound = 1
            if duplicateFound == 0:
                listOfAverages.append(i)
        pl = {'listOfAverages' : listOfAverages}
        http = HttpResponse(json.dumps(pl))
        http['Content-Type'] = 'application/json'
        http.status_code = 200
        http.reason_phrase = 'OK'
        return http
    else:
    #if post tell client wrong request
        http = HttpResponseBadRequest()
        http['Content-Type'] = 'text/plain'
        http.content = "Bad Request, only get allowed."
        return http

@csrf_exempt
#average rating of given professor for given module
def averageRating(request):
#check post request
    if request.method == 'POST':
    #get details of post
        module = request.POST.get('module')
        professor = request.POST.get('professor')
        professorObj = Professor.objects.get(code=professor)
        moduleObj = Module.objects.all().filter(code=module)
        counter = 0
        total = 0
        moduleName = ""
        #calculate average for given details, add to json list and send to client
        for obj in moduleObj:
            allRatings = Rating.objects.filter(professor=professorObj, module=obj).values('rating')
            moduleName = obj.name
            for rating in allRatings:
                counter += 1
                total += int(rating['rating'])
        average = Decimal(total/counter).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)
        listOfAverages = []
        i = {'professorName': professorObj.name, 'professorCode' : professor, 'moduleName' : moduleName, 'moduleCode' : module, 'average' : int(average)}
        listOfAverages.append(i)
        if(len(listOfAverages) != 1):
            return HttpResponse("No Match Found")
        pl = {'listOfAverages' : listOfAverages}
        http = HttpResponse(json.dumps(pl))
        http['Content-Type'] = 'application/json'
        http.status_code = 200
        http.reason_phrase = 'OK'
        return http

@csrf_exempt
#rate teacher function
def rateTeacher(request):
#check for post request
    if request.method == 'POST':
    #get details passed to the function
        professor = request.POST.get('professor')
        module = request.POST.get('module')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        username = request.POST.get('username')
        password = request.POST.get('password')
        rating = int(request.POST.get('rating'))
	#check each value if in database add to rating, else return not found, client handles that, repeat for professors, modules and student
        allProfessors = Professor.objects.all().values('id', 'code')
        profId = None
        for prof in allProfessors:
            if prof['code'] == professor:
                profId = prof['id']
                break

        if(profId == None):
            return HttpResponse("Not Found")


        moduleId = None
        module = Module.objects.get(code=module, year=year, semester=semester)
        if(len(module.taughtBy.filter(id=profId)) == 1):
            moduleId = module.id


        if(moduleId == None):
            return HttpResponse("Not Found")

        allStudents = Student.objects.all().values('id', 'username', 'password')
        studentId = None
        for student in allStudents:
            if student['username'] == str(username):
                if student['password'] == str(password):
                    studentId = student['id']
                    break


        student = Student.objects.get(id=studentId)
        module = Module.objects.get(id=moduleId)
        professor = Professor.objects.get(id=profId)
        rating = Rating.objects.create(professor=professor,student=student, module=module, rating=rating)
        return HttpResponse('OK')
