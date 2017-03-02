import json
import string
from pylab import *
from datetime import datetime


def max(listname):
    maxvalue=0
    for i in listname:
        if maxvalue <= i:
            maxvalue=i
    return maxvalue

textfile=open("term_frequencies.txt", "w+")
textfile2=open("term_frequencies_overtime.txt", "w+")
textfile3=open("term_cooccurrences.txt", "w+")


#PART1

punctuation = list(string.punctuation)
stop = punctuation+[ 'a','an','the','rt', 'via','to','of','for','and','or','i','in','at','on','out','with','by','de',' ','is','am','are','my','your','our','us','me','you','it','','the','no','have','has','we','her','his','them','when','who','where','which','how','that','not','this','&amp;','https','from','new','la','but']

tweetdict={}
hourlist=[]
minutelist=[]
dt_ws_list=[]

jsonf=open('tweet_data.json', 'r')
for lines in jsonf:
    tweet = json.loads(lines)
    created_at_format = '%a %b %d %H:%M:%S +0000 %Y'
    strtweet=tweet['text']
    strtweet=strtweet.lower()
    splittweet=strtweet.split(" ")
    date=tweet["created_at"]
    dt=datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")
    dt_ws=dt.replace(second=0,microsecond=0)
    dateoftheday=(str(dt.year)+ "-" +str(dt.month)+"-"+str(dt.day))
    if dt_ws not in dt_ws_list:
        dt_ws_list.append(dt_ws)


    for i in splittweet:
        if i not in stop:
            try:
                tweetdict[i]+=1
            except KeyError:
                tweetdict[i]=1


    if dt.hour not in hourlist:
        hourlist.append(dt.hour)
    if dt.minute not in minutelist:
        minutelist.append(dt.minute)

strtweetdict={}
for el in tweetdict.keys():
    strtweetdict[tweetdict[el]]= el

tweetnums=tweetdict.values()

maxtweetnums=[]
for k in range(20):
    maxtweetnums.append(max(tweetnums))
    tweetnums.remove(max(tweetnums))

maxtweets=[]
for k in tweetdict.keys():
    if tweetdict[k] in maxtweetnums:
        if k not in maxtweets:
            maxtweets.append(k)
            with open("term_frequencies.txt", "a+") as textfile:
                textfile.write("' " + k + " '" + "  - " + str(tweetdict[k]) + " times" + "\n" )


maxtweets_forbar=[]
for j in maxtweetnums:
    for i in maxtweets:
        if j==tweetdict[i]:
            if i not in maxtweets_forbar:
                maxtweets_forbar.append(i)

fig = plt.figure()
width = 8
loc = np.arange(len(maxtweetnums))
plt.ylabel('Tweet Frequencies')
plt.title('Tweet Mining Graph')
plt.bar(loc, maxtweetnums)
plt.xticks(loc + width/8.,maxtweets_forbar)
plt.yticks(np.arange(0,maxtweetnums[0]+100, 100))
fig.autofmt_xdate()
plt.savefig('term_frequencies.png')


#PART2

maxtweetnums2=maxtweetnums[:5]
maxstrtweet=[strtweetdict[i] for i in maxtweetnums2]

lastlistfortimebar=[]
for k in maxstrtweet:
    firstlistfortimebar=[]
    datedict={}
    jsonf=open('tweet_data.json', 'r')
    for lines in jsonf:
        tweet = json.loads(lines)
        created_at_format = '%a %b %d %H:%M:%S +0000 %Y'
        strtweet=tweet['text']
        strtweet=strtweet.lower()
        splittweet=strtweet.split(" ")
        date=tweet["created_at"]
        dt=datetime.strptime(date, "%a %b %d %H:%M:%S +0000 %Y")

        for t in hourlist:
            if t==dt.hour:
                for m in minutelist:
                    if m==dt.minute:
                        for j in splittweet:
                            if k==j:
                                try:
                                    datedict[str(t)+str(m)]+=1
                                except KeyError:
                                    datedict[str(t)+str(m)]=1

    for t in hourlist:
        for m in minutelist:
            try:
                firstlistfortimebar.append(datedict[str(t)+str(m)])
            except KeyError:
                pass

    lastlistfortimebar.append(firstlistfortimebar)

    for h in hourlist:
        for m in minutelist:
            if int(m)>=10:
                try:
                    with open("term_frequencies_overtime.txt", "a+") as textfile2:
                        textfile2.write(k+ " " + dateoftheday +" "+str(h)+":"+str(m)+":00"+ " " + str(datedict[str(h)+str(m)]) + "\n" )

                except KeyError:
                    pass
            else:
                try:
                    with open("term_frequencies_overtime.txt", "a+") as textfile2:
                        textfile2.write(k+ " " + dateoftheday +" "+str(h)+":0"+str(m)+":00"+ " " + str(datedict[str(h)+str(m)]) + "\n" )

                except KeyError:
                    pass

x1=dt_ws_list
y1=lastlistfortimebar[0]

x2=dt_ws_list
y2=lastlistfortimebar[1]

x3=dt_ws_list
y3=lastlistfortimebar[2]

x4=dt_ws_list
y4=lastlistfortimebar[3]

x5=dt_ws_list
y5=lastlistfortimebar[4]

fig=plt.figure()
plt.plot(x1,y1,label=maxstrtweet[0])
plt.plot(x2,y2,label=maxstrtweet[1])
plt.plot(x3,y3,label=maxstrtweet[2])
plt.plot(x4,y4,label=maxstrtweet[3])
plt.plot(x5,y5,label=maxstrtweet[4])
plt.xlabel("Time")
plt.ylabel("Frequency of Occurrence")
plt.legend()
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.savefig("term_frequencies_overtime.png")


#PART3

maxtweetnums3=maxtweetnums[:10]

maxstrtweet3=[strtweetdict[elmn] for elmn in maxtweetnums3]

linetweetlist=[]
jsonf=open('tweet_data.json', 'r')
for lines in jsonf:
    tweet = json.loads(lines)
    created_at_format = '%a %b %d %H:%M:%S +0000 %Y'
    strtweet=tweet['text']
    strtweet=strtweet.lower()
    splittweet=strtweet.split(" ")
    linetweet=[i for i in splittweet if i not in stop]
    linetweetlist.append(linetweet)


matrixlist=[]
for k in maxstrtweet3:
    tweetcounterlist=[]
    for j in maxstrtweet3:
        tweetcounter=0
        for line in linetweetlist:
            if k in line:
                if j in line:
                    tweetcounter+=1

        with open("term_cooccurrences.txt", "a+") as textfile3:
            textfile3.write(k + "-" + j + " , " + str(tweetcounter) + " times" + "\n")


        tweetcounterlist.append(tweetcounter)
    matrixlist.append(tweetcounterlist)


Conf_Emty_List = []
for i in matrixlist:
    n = 0
    ARRA = []
    n = sum(i, 0)
    for k in i:
        ARRA.append(float(k))
    Conf_Emty_List.append(ARRA)

fig = plt.figure()
plt.clf()
ax = fig.add_subplot(111)
ax.set_aspect(1)
res = ax.imshow(np.array(Conf_Emty_List), cmap=plt.cm.jet,
                interpolation='nearest')

width = len(matrixlist)
height = len(matrixlist[0])

for x in xrange(width):
    for y in xrange(height):
        ax.annotate(str(matrixlist[x][y]), xy=(y, x),
                    horizontalalignment='center',
                    verticalalignment='center')

cb = fig.colorbar(res)
alphabet = maxstrtweet3
fig.autofmt_xdate()
plt.xticks(range(width), alphabet[:width])
plt.yticks(range(height), alphabet[:height])
plt.savefig('term_cooccurrences.png', format='png')































































