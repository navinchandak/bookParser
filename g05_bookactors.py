from fileparser import lineread

def title_author(f):
	while(1):
		line=f.readline()
		if(line.startswith('Title:')):
			words=line.split()
			title=""
			for i in range(1,len(words)):
				title+=words[i]+" "
			print "Title of Author: ",title
		if(line.startswith('Author:')):
			words=line.split()
			author=""
			for i in range(1,len(words)):
				author+=words[i]+" "
			print "Name of author",author
		if(line.lower().find("contents")!=-1):
			##so start parsing word by word
			break;
def terminationCon(line):
	if(line.lower().find("end of project gutenberg's")!=-1):
		return 1
	else:
		return 0
def getWord(word):
	word=(word.split(',')[0]).split("'")[0].split(";")[0]
	return word
def capitalBlock(words,index):
	i=index
	capitalWords=[]
	while(i<len(words) and (words[i]=="and" or words[i][0]!=words[i][0].lower())):
		if(words[i]=="and"):
			capitalWords[-1]+=","
		else:
			capitalWords.append(words[i])
		if(words[i].find("'")!=-1):
			i=i+1
			break
		else:
			i=i+1
	returnlist=[]
	curr_list=[]
	for word in capitalWords:
		if(word.find(",")!=-1 or word.find(";")!=-1):
			curr_list.append(word)
			returnlist.append(curr_list)
			curr_list=[]
		else:
			curr_list.append(word)
	if curr_list:
		returnlist.append(curr_list)
	while(i<len(words) and words[i][0]==words[i][0].lower()):
		i=i+1
	return {'index':i,'list':returnlist}
def is_number(word):
	try:
		float(word)
		return True
	except ValueError:
		return False
def ignoreCon(line):
	for word in line:
		if(len(word)>0 and (not (word.isdigit())) and  word.lower()==word):
			return 0
	return 1
lineMaleIndicators=['he','his','him','himself']
lineFemaleIndicators=['she','her','hers','herself']
articlesAgainstChar=['a','an','these','Mt.']
conditionalArticlesAgainstChar=['at','in']
wordsAgainstChar= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',
'January','February','March','April','May','June','July','August','September','October','November','December']
postMaleIndicators=['himself']
postFemaleIndicators=['herself']
maleIndicators=['Mr.','Master','Mister','Uncle','Sir']
femaleIndicators=['Mrs.','Miss','Ms.','Aunt','Madam']
charIndicators=['i','my','my','mine','mother','father','grandmother','grandmother','friend']
charIndicators.extend(lineMaleIndicators)
charIndicators.extend(lineFemaleIndicators)
forChar=['Dr.','Doctor','Prof.','Professor','Saint','St.','Gen.','Fr.','Father','General','Sen.']
forChar.extend(maleIndicators)
forChar.extend(femaleIndicators)
postForChar=[]
postForChar.extend(postMaleIndicators)
postForChar.extend(postFemaleIndicators)
def updateGenderHints(words,capital_block):
	capital_block_temp=[]
	for entity in capital_block:
		i=stringIndex(words,entity[-1])
		if(entity[0] in maleIndicators):
			capital_block_temp.append({'gender':'male','name':entity})	
		elif(entity[0] in femaleIndicators):
			capital_block_temp.append({'gender':'female','name':entity})
		elif(i+1<len(words) and words[i+1] in postMaleIndicators):
			capital_block_temp.append({'gender':'male','name':entity})
		elif(i+1<len(words) and words[i+1] in postFemaleIndicators):
			capital_block_temp.append({'gender':'female','name':entity})
		else:
			capital_block_temp.append({'gender':'notsure','name':entity})
	return capital_block_temp

def addToCharList(words,capital_block):
	found=0
	capital_block_temp=[]
	for entity in capital_block:
		flag=0
		for x in entity['name']:
			y=getWord(x)
			if(y=="I" or y=="Oh"):
				flag=1
		if flag==0:
			capital_block_temp.append(entity)
	capital_block=capital_block_temp
	if(not capital_block):
		found=4
	for entity in capital_block:
		r1=search(entity['name'],'confirm')
		r2=search(entity['name'],'not')
		if(r1!=-1):
			addList('confirm',capital_block)
			found=1
			break
		elif(r2!=-1):
			addList('not',capital_block)
			found=2
			break
	#####look for hints here 
	##char is there in maybe list or else not there
	if found==0:
		capital_block_temp=[]
		for entity in capital_block:
			if(stringIndex(words,entity['name'][0])==0 and len(entity['name'])==1 and (search(entity['name'],'maybe')==-1)):
				continue
			capital_block_temp.append(entity)
		capital_block=capital_block_temp
		if(not capital_block):
			found=4
	if(found==0):
		for entity in capital_block:
			if(entity['name'][0] in forChar):
				found=1
				addList('confirm',capital_block)
				break
	if(found==0):
		for entity in capital_block:
			i=stringIndex(words,entity['name'][-1])
			if(i+1<len(words) and words[i+1] in postForChar):
				found=1
				addList('confirm',capital_block)
				break
	if(found==0):
		if((i>=1 and words[i-1] in articlesAgainstChar) or (i>=2 and words[i-2] in articlesAgainstChar)):
			addList('not',capital_block)
			found=2
	if(found==0):
		for entity in capital_block:
			for x in wordsAgainstChar:
				if(getConcateneted(entity['name']).find(x)!=-1):
					addList('not',capital_block)
					found=2
					break
	#put it in the maybe list
	#print "capital block",capital_block
	#print len(capital_block[0])
	if(found==0):
		addList('maybe',capital_block)
		found=3
	return found
def updateGenderIfNecessary(words,active_char,seperator):
	if(active_char and seperator==1):
		for word in words:
			y=word.split(',')[0].lower()
			if (y in lineMaleIndicators):
				updateGender(active_char['name'],'male')
				return
			elif (y in lineFemaleIndicators):
				updateGender(active_char['name'],'female')
				return
def stringIndex(words,word):
	for x in range(len(words)):
		if(words[x]==word):
			return x
	return -1
def findNumChars(words):
	num_active_chars=0
	for word in words:
		x=word.split(',')[0].lower()
		if x in charIndicators:
			num_active_chars += 1
	return num_active_chars
def printCharList():
	return
	print "---CHARLIST------"
	for i in charList:
		print i
	print "------------------"
def returnConfirmCharList():
	confirmList=[]
	for i in charList:
		if(i['status']=='confirm'):
			confirmList.append(i)	
	return confirmList
def printMaybeCharList():
	return
	print "---CHARLIST------"
	for i in charList:
		if(i['status']=='maybe'):
			print i	
	print "------------------"
def preetham(f):
	s="The cat and kitten were both eating supper and Navin, Hardik, and Preetham Sreenivas Christmas was watching them"
	return s
def main():
	a='novel.txt'
	a = raw_input("What is the name of text file? ")
	f = open( a, 'r')
	title_author(f)
	active_char=[]
	num_active_char=0
	while(True):
		########parse a line..
		line_n_seperator=lineread(f)
		line=line_n_seperator['string']
		seperator=line_n_seperator['num']
		words=line.split()
		##termination condition or ignore condition
		terminate=terminationCon(line)
		if(terminate==1):
			break
		ignore=ignoreCon(words)
		if(ignore==1):
			continue
		printCharList()
		## Update gender__ active wala algorithm -- if I can infer someone's gender from this line
		prev_active_char=active_char
		active_char=[]
		num_active_chars=0
		i=0
		##reach first capital letter or the end if no capital letters are found
		while(i<len(words) and  (words[i][0]==words[i][0].lower())):
			i+=1
		while(i!=len(words)):
			capital_block_pair=capitalBlock(words,i)
			capital_block=capital_block_pair['list']
			found=0
			#####look for gender hints
			capital_block=updateGenderHints(words,capital_block)
			if(i==0 and bestMatch(capital_block[0]['name'],'confirm')==-1):
				for x in capital_block:
					found=addToCharList(words,[x])
					if(found==1 or found==3):
						num_active_chars+=1
						last_character=x
			else:
				found=addToCharList(words,capital_block)
				if(found==1 or found==3):
					num_active_chars+=len(capital_block)
					last_character=capital_block[-1]
			i=capital_block_pair['index']
		##I have parsed the entire line by here
		if(num_active_chars==0):
			updateGenderIfNecessary(words,prev_active_char,seperator)
		num_active_chars+=findNumChars(words)
		if(seperator==1 and num_active_chars==1):
			active_char=last_character
	#printMaybeCharList()
	#printConfirmCharList()
	for x in charList:
		print x['name'],"         ",x['gender'],"       ",x['count'],"     ",x['status']
	print
	tempList=returnConfirmCharList()
	newTempList = sorted(tempList, key=lambda k: k['name'])
	print
	print "Characters with name, and gender"
	for x in newTempList:
		print x['name'],"         ",x['gender'],"       ",x['count']
	print
	maxCountMale=-1
	maxCountMaleIndex=-1
	maxCountFemale=-1
	maxCountFemaleIndex=-1
	for i in range(len(charList)):
		char=charList[i]
		if(char['status']=='confirm'):
			if(char['gender']=='male' and char['count']>maxCountMale):
				maxCountMale=char['count']
				maxCountMaleIndex=i
			if(char['gender']=='female' and char['count']>maxCountFemale):
				maxCountFemale=char['count']
				maxCountFemaleIndex=i
	maxCountVillian=-1
	maxCountVillianIndex=-1
	for i in range(len(charList)):
		char=charList[i]
		if(char['status']=='confirm'):
			if(i!=maxCountMaleIndex and i!=maxCountFemaleIndex):
				if(char['count']>maxCountVillian):
					maxCountVillian=char['count']
					maxCountVillianIndex=i
	print		
	print "Hero of the novel:",charList[maxCountMaleIndex]['name']
	print "Heroine of the novel:",charList[maxCountFemaleIndex]['name']
	print "Villian of the novel:",charList[maxCountVillianIndex]['name']

charList=[
#{'name':'Ted Turner','gender':'notsure','count':1,'status':'confirm','lcount':0},
			]

ucount=0 
def getConcateneted(name):
	ret=''
	for x in name:
		if(ret==''):
			ret+=x
		else:
			ret+=" "+x
	return ret
def remove_title(nameList):
	newList=[]
	newList.extend(nameList)
	if(newList[0] in forChar):
		newList=newList[1:]
	return newList
def search(name,status):
	return bestMatch(name,status)
def bestMatch(name,status=''):
	temp_list=remove_title(name)
	temp=[]
	for x in temp_list:
		temp.append(getWord(x))
	if(not temp):
		return -1
	name_str=getConcateneted(temp)
	for i in range(len(charList)):
		char=charList[i]
		if(status!='' and char['status']!=status):
			continue
		char=charList[i]
		if(name_str==char['name']) and noGenderMismatch(char['gender'],name):
			return i
	for i in range(len(charList)):
		char=charList[i]
		if(status!='' and char['status']!=status):
			continue
		if(temp[0]==char['name'].split()[0] and noGenderMismatch(char['gender'],name)):
			return i
	maxi=-1
	maxv=-1
	for i in range(len(charList)):
		char=charList[i]
		if(status!='' and char['status']!=status):
			continue
		if((' '+char['name']+' ').find(' '+name_str+' ')!=-1 and noGenderMismatch(char['gender'],name)):
			if(char['lcount']>maxv):
				maxv=char['lcount']
				maxi=i
	return maxi
def noGenderMismatch(cgender,name):
	if(not name):
		return True
	if(cgender=='male' and (name[0] in femaleIndicators)):
		return False
	if(cgender=='female' and (name[0] in maleIndicators)):
		return False
	return True
def addList(status,capital_block):
	global ucount
	for entity in capital_block:
		x=searchAndAdd(status,entity)
		if(x==0):
			ucount+=1
			name=getWord(getConcateneted(remove_title(entity['name'])))
			if(name!=''):
				charList.append({'name':name,'gender':entity['gender'],'count':1,'lcount':ucount,'status':status})
def searchAndAdd(status,char):
	global ucount
	f_flag=0 
	i=bestMatch(char['name'])
	if(i!=-1):
		listP=charList[i]
		listP['count']+=1
		ucount+=1
		listP['lcount']=ucount
		listP['status']=status
		if(listP['gender']=='notsure'):
			listP['gender']=char['gender']
		return 1
	else :
		return 0
def updateGender(name,gender):
	index=bestMatch(name)
	if(index!=-1 and charList[index]['gender']=='notsure'):
		charList[index]['gender']=gender
''' 
print remove_title(['Mr.','Navin','Chandak'])
print bestMatch(['Mr.','Ted','Turner'])
print search(['Mr.','Ted','Turner'],'confirm')
updateGender(['Mr.','Ted','Turner'],'male')
print searchAndAdd('confirm',{'gender':'male','name':['Tur']})
print addListIfPresent('confirm',[{'gender':'male','name':['Navin']}])
print charList
'''
main()
