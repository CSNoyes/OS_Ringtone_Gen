import sys ; import getopt ; import re
import urllib.request

def dictionarySelector(gender): #create global dics for urls and stuff
	global selectedReasonDic ; global selectedEndingDic
	global selectedReasonKeys ; global selectedEndingKeys
	if gender.lower() == "m":
		selectedReasonDic = reasonsM ; selectedEndingDic = endingsM
		selectedReasonKeys = list(reasonMKeys) ; selectedEndingKeys = list(endingMKeys)

	if gender.lower() == "f":
		selectedReasonDic = reasonsF ; selectedEndingDic = endingsF
		selectedReasonKeys = list(reasonFKeys) ; selectedEndingKeys = list(endingFKeys)

def main(): #if no arguments, runs the program
	print("Hello, welcome to the old spice voicemail generator. \n" )
	gender,number,reason,ending,output = inputHandler()
	finalWrite(gender,number,reason,ending,output)

def inputHandler(): #takes user input
	gender = genderCheck()
	number = numberInput()
	dictionarySelector(gender)
	reason = reasonSelect()
	ending = endingSelect()
	output = outputSelect()
	return gender,number,reason,ending,output

def genderCheck(): #checks gender for validity/takes input
	try:
		gender = str(input("Please specify your gender (M/F): "))
		if gender.lower() == "m":
			return "m"
		elif gender.lower() == "f":
			return "f"
		else:
			print("You fucked goofed, bruh.")
			genderCheck()
	except:
		print("There was an error.")
		genderCheck()

def numberInput(): #phone number input taker
	number = input("Please enter your number: ")
	number = re.sub('[^0-9]','', number)
	lenNumber = len(number)
	if lenNumber != 10:
		print("This isn't a valid number.")
		numberInput()
	return number

def reasonSelect(): #takes reason input
	print("\n")
	for reasons in selectedReasonKeys:
		print (reasons + "[" + str(selectedReasonKeys.index(reasons)) + "]")
	reason = int(input("\n Please enter the number of the reason you want: "))
	if reason == 0 or reason == 1 or reason == 2 or reason == 3 or reason == 4:
		return selectedReasonKeys[reason]
	else:
		print("Bruh you goofed. Try again.")
		reasonSelect()

def endingSelect(): #ending input taker
	for reasons in selectedEndingKeys:
		print (reasons + "[" + str(selectedEndingKeys.index(reasons)) + "]")
	print("\n")
	ending = int(input("Please enter the number of the ending you want: "))
	if ending == 0 or ending == 1 or ending == 2:
		return selectedEndingKeys[ending]
	else:
		print("Bruh you goofed. Try again.")
		endingSelect()

def outputSelect(): #output input (haha) taker
	try:
		output = input("\nWhat would you like your file to be named?: ")
		if output.endswith(".mp3"):
			return output
		else:
			return (output + ".mp3")
	except:
		print("Error, try again.")
		outputSelect()

def finalWrite(gender,number,reason,ending,output): #writes the given values to the output file
	reasonURL = selectedReasonDic[reason]
	endingURL = selectedEndingDic[ending]
	fileObject = open(output,"wb+")
	if gender.lower() == "m":
		tempObject = urllib.request.urlopen(urlPath+"beginningMale.mp3").read()
		fileObject.write(tempObject)
	elif gender.lower() == "f":
		tempObject = urllib.request.urlopen(urlPath+"beforeReasonF.mp3").read()
		fileObject.write(tempObject)
	for digit in list(str(number)):
		tempObject = urllib.request.urlopen(urlPath+digit+".mp3").read()
		fileObject.write(tempObject)
	if gender.lower() == "m":
		tempObject = urllib.request.urlopen(urlPath+"beforeReasonM.mp3").read()
		fileObject.write(tempObject)
	tempObject = urllib.request.urlopen(urlPath+reasonURL).read()
	fileObject.write(tempObject)
	if gender.lower() == "m":
		tempObject = urllib.request.urlopen(urlPath+"afterReasonM.mp3").read()
		fileObject.write(tempObject)
	tempObject = urllib.request.urlopen(urlPath+endingURL).read()
	fileObject.write(tempObject)
	if gender.lower() == "m":
		tempObject = urllib.request.urlopen(urlPath+"finalEndM.mp3").read()
		fileObject.write(tempObject)
	elif gender.lower() == "f":
		tempObject = urllib.request.urlopen(urlPath+"afterEndingF.mp3").read()
		fileObject.write(tempObject)
	tempObject = urllib.request.urlopen(urlPath+"spiceTone.mp3").read()
	fileObject.write(tempObject)
	if gender == "m":
		gender = "male"
	else:
		gender = "female"
	print(gender,",",number,",",reason,",",ending,",",output)

if __name__ == "__main__": #run at program start and checks to see if there are command line args
	global reasonsM ; reasonsM = {"Polishing their monocle" : "rMonocleM.mp3", "Building an orphanage" : "rOrphanageM.mp3","Cracking walnuts" : "rWalnutsM.mp3", "Lifting weights" : "rWeightsM.mp3"}
	global reasonsF ; reasonsF = {"Riding a horse" : "rHorseF.mp3", "Eating lobster" : "rLobsterF.mp3", "On the moon sharing a kiss" : "rMoonF.mp3", "Being read poetry" : "rPoetryF.mp3", "Ingesting delicious man-smell" : "rSmellF.mp3"}
	global reasonMKeys; reasonMKeys = reasonsM.keys() ; global reasonFKeys ; reasonFKeys = reasonsF.keys()
	global endingsM ; endingsM = {"I'm on a horse" : "eHorseM.mp3", "Swan dive!" : "eSwanM.mp3", "I'm on a phone" : "ePhoneM.mp3"}
	global endingsF ; endingsF = {"Unable to take your call" : "eUnable.mp3", "She's busy" : "eBusyF", "Both of those" : "eBothF.mp3"}
	global endingMKeys; endingMKeys = endingsM.keys() ; global endingFKeys ; endingFKeys = endingsF.keys()
	global urlPath; urlPath = "http://charlien.me/oldspice/"
	if len(sys.argv) != 1:
		try:
			opts,args = getopt.getopt(sys.argv[1:], "g:n:r:e:o:")
		except getopt.GetoptError as error:
			print(error)
			print("Your arguments were wrong.")
		for opt,arg in opts:
			if opt in "-g":
				if str(arg).lower() == "m":
					gender = "m"
				elif str(arg).lower() == "f":
					gender = "f"
				else:
					print("Error. Your input is invalid")
				dictionarySelector(gender)
			elif opt in "-n":
				number = arg
			elif opt in "-r":
				reason = arg
				reason = selectedReasonKeys[reason]
			elif opt in "-e":
				ending = arg
				ending = selectedEndingKeys[ending]
			elif opt in "-o":
				output = arg
		finalWrite(gender,number,reason,ending,output)
	else:
		main()