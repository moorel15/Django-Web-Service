import requests
import json
import sys

loggedIn = False
userLoggedIn = ""
userLoggedInPass = ""

#loop continously for input
while 1 == 1:
    while 1 == 1:
    #prit available commands
        print('\n\nAvailable commands:\n\nregister\nlogin\nlogout\nlist\nview\naverage\nrate\nexit\n\n')
        #ask for input
        command = input('Type the name of the service you require.\n')
        #determine command type, act upon that.
        if(command == 'register'):
        #ask for registration inputs, send them wait for response, decide if user is registered.
            name = input("Please enter your full name: ")
            username = input("Please input a username of your choice: ")
            email = input("Please input an email of your choice: ")
            password = input("Please input a password of your choice: ")
            detailsRequest = {'name': str(name), 'username' : str(username), 'email' : str(email), 'password' : str(password)}
            r = requests.post('http://sc17lm.pythonanywhere.com/api/register', data=detailsRequest)
            if r.text == 'OK':
                print("\n\nSuccessful registered, now log on.\n")
                print("........................................")
            else:
                print("\n\nUnsuccesful registration, please try different " + str(r.text))
                print("..........................................................................")
        elif(command == 'login'):
        #check if a user is already logged in.
            if loggedIn:
                print("\n\n" + userLoggedIn + " is already logged in please log out.")
                print("....................................................................")
                break
            else:
            #get all inputs for login, send to server, wait for response and log user in accordingly
                username = input("Please input your username: ")
                password = input("Please input your password: ")
                loginRequest = {'username' : str(username), 'password' : str(password)}
                r = requests.post('http://sc17lm.pythonanywhere.com/api/login', data=loginRequest)
                if r.text == 'OK':
                    print("Successfully logged in.\n")
                    loggedIn = True
                    userLoggedIn = str(username)
                    userLoggedInPass = str(password)
                elif r.text == 'No Match':
                    print("Credentials do not match. Please try again.\n")
        elif(command == 'logout'):
        #check if someone is logged in, if yes ask for password to log out.
            if loggedIn:
                password = input("\n\nIn order to log out please input password: ")
            if(password == userLoggedInPass):
                print("\n\nSuccessfully Logged out.")
                print(".............................")
                loggedIn = False
                userLoggedInPass = ""
                userLoggedIn = ""
        elif(command == 'list'):
        #send get request wait for json and display in specified format
            r = requests.get('http://sc17lm.pythonanywhere.com/api/list')
            if r.text == "Bad Request, only get allowed.":
                print(r.text)
            else:
                data = json.loads(r.text)
                print("\n\n%-4s %-40s %-4s %-8s %-50s" % ("Code", "Name", "Year", "Semester", "Taught By"))
                for i in data['listOfModules']:
                    code = i['code']
                    name = i['name']
                    year = i['year']
                    semester = i['semester']
                    taughtBy = i['taughtBy']
                    print("%4s %-40s %-4s %-8s %-50s" % (code, name, str(year), str(semester), taughtBy))
                    print(".....................................................................................................")
        elif(command == 'view'):
        #send get request and wait for json and display in specified format.
            r = requests.get('http://sc17lm.pythonanywhere.com/api/ratings')
            if r == "Bad Request, only get allowed.":
                print(r.text)
            else:
                data = json.loads(r.text)
                for i in data['listOfAverages']:
                    code = i['code']
                    name = i['name']
                    rating = i['average']
                    print("\n\nThe rating of " + str(name) + "(" + str(code) + ") is: " + "*" * int(rating))
                    print("..........................................................................")
        elif(command == 'average'):
        #ask for input needed to get average, send post request with that information
            professor = input("Please input professor code (eg. TT1): ")
            module = input("Please input module code (eg. CD1): ")
            averageRequest = {'professor' : str(professor), 'module' : str(module)}
            r = requests.post('http://sc17lm.pythonanywhere.com/api/average', data=averageRequest)
            if (r.reason == 'OK'):
            #get response and display for given format. If not given then display message
                data = json.loads(r.text)
                for i in data['listOfAverages']:
                    professorName = i['professorName']
                    professorCode = i['professorCode']
                    moduleName = i['moduleName']
                    moduleCode = i['moduleCode']
                    rating = i['average']
                print("\n\nThe rating of " + str(professorName) + " (" + str(professorCode) + ") in the module " + str(moduleName) + " (" + str(moduleCode) + ") is: " + ("*" * int(rating)))
                print("...................................................................................................................")
            else:
                print("\n\nThe inputted values did not yeild an average, perhaps the professor does not teach that module.")
                print("...................................................................................................................")
        elif(command == 'rate'):
        #check if user is logged in to rate.
            if not loggedIn:
                print("\n\nPlease login in order to rate a professor.")
                print("..............................................")
                break
            else:
            #ask for inputs for rating
                professor = input("Please input professor code (eg. TT1): ")
                module = input("Please input module code (eg. CD1): ")
                year = input("Please input the year of the module (eg. 2018): ")
                semester = input("Please input a semester (1 or 2): ")
                rating = input("Please input your rating (1-5): ")
                try:
                #check numerical inputs
                    if (int(rating) < 1):
                        print("\n\nIncorrect data presented, please try again.")
                        print("..............................................")
                    elif (int(rating) > 5):
                        print("\n\nIncorrect data presented, please try again.")
                        print("..............................................")
                except ValueError:
                    print("Rating must be integer 1-5")
                else:
                #build rating request and send in request
                    ratingRequest = {'professor' : str(professor).upper(), 'module' : str(module).upper(), 'year' : year, 'semester' : semester, 'rating' : rating, 'username' : userLoggedIn, 'password' : userLoggedInPass}
                    r = requests.post('http://sc17lm.pythonanywhere.com/api/rate', data=ratingRequest)
                    if r.text == 'OK':
                    #print message based on server response
                        print("\n\nRating Successfully submitted.")
                        print("..............................")
                    else:
                        print("\n\nDetails submitted did not match either module(name, year or semester) or professor in our database.")
                        print("...................................................................................................................")
        elif(command == 'exit'):
        #exit program
            exit()
        else:
        #ask for another command if invalid.
            print('\n\nInvalid command try again.')
            print("..............................")
