import urllib2
import datetime
import sys
import sqlite3

path = '/var/www/'

class Info:
    def __init__(self):
        self.close        = 0
        self.high         = 0
        self.stock        = ""
        self.currentClose = 0

        self.date         = ""
        self.highDate     = ""
        self.closeDate    = ""


#Creates an HTML page with the stock information organized into a table.
def MakeHTMLTable(a,b,c,d,e,f,infoList):
    page = open(path + "table.html" , "w")
    page.write("<html><head><script src=\"jquery-1.9.1.min.js\"></script>\n")
    page.write("<script src=\"test-jquery.js\"></script>")
    page.write("</head>\n<body>\n")

    page.write("<table border=\"1\">\n")
    page.write('<tr><td>Stock</td><td>Current Close</td><td>High Close</td><td>2%</td><td>4%</td></tr>')

    for info in infoList:
        x = float(info.close) - (float(info.close) * .02)
        y = float(info.close) - (float(info.close) * .04)

        page.write("<tr>\n")
        page.write("<td id=\"" + info.stock + "\" class=\"stock\">" + info.stock + "</td>\n")
        page.write("<td>" + str(info.currentClose) + "</td>\n")
        page.write("<td>" + str(info.close) + "</td>\n")
        #page.write("<td>" + str(info.high) + "</td>\n")
        page.write("<td id=\"" + info.stock + "1\"> " + str(x) + " </td>\n")
        page.write("<td id=\"" + info.stock + "2\"> " + str(y) + " </td>\n")
        page.write("</tr>\n")

    current = datetime.datetime.now()

    page.write("</table>\n")
    page.write("<p>Last run on: " + current.strftime("%Y-%m-%d %H:%M") + "</p>")
    page.write('<a href="list.html">Go to list</a>')
    page.write("</body></html>")
    page.close()


def MakeHTMLList(a,b,c,d,e,f,infoList):
    page = open(path + "list.html" , "w")
    page.write("<html><head><script src=\"jquery-1.9.1.min.js\"></script>\n")
    page.write("<script src=\"test-jquery.js\"></script>")
    page.write("</head>\n<body>\n")

    page.write("<p> Stock info </p>\n")

    for info in infoList:
        x = float(info.close) - (float(info.close) * .02)
        y = float(info.close) - (float(info.close) * .04)

        page.write('<div id="' + info.stock + 'info">')
        page.write("Stock: " + info.stock + "<br />")
        page.write("Last close: " + str(info.currentClose) + " -- Date: " + info.date + "<br />") 
        page.write("High close: " + str(info.close) + " -- Date: " + info.closeDate + "<br />")
        #page.write("High high: " + str(info.high) + " -- Date: " + info.highDate + "<br />") 
        page.write('<div id="' + info.stock + '1"> 2%: ' + str(x) + '</div>')
        page.write('<div id="' + info.stock + '2"> 4%: ' + str(y) + '</div>')
        page.write('<br />')
        page.write('</div>')

    current = datetime.datetime.now()

    page.write("<p>Last run on: " + current.strftime("%Y-%m-%d %H:%M") + "</p>")
    page.write('<a href="table.html">Go to table</a>')
    page.write("</body></html>")
    page.close()


#a,d month
#b,e day
#c,f year
def getStockPrices(a,b,c,d,e,f,stock):
    #bah = "http://ichart.finance.yahoo.com/table.csv?s=" + stock + "&a=" + str(a) + "&b=" + str(b) + "&c=" + str(c) + "&d=" + str(d) + "&e=" + str(e) + "&f=" + str(f) + "&g=d&ignore=.csv"
    #print bah
    
    #This URL returns the columns in the following order:
    #Date, Open, High, Low, Close, Volume, Adj Close
    f = urllib2.urlopen("http://ichart.finance.yahoo.com/table.csv?s=" + stock + "&a=" + str(a) + "&b=" + str(b) + "&c=" + str(c) + "&d=" + str(d) + "&e=" + str(e) + "&f=" + str(f) + "&g=d&ignore=.csv")

    content = f.readline()  #Throw away the first line with column names.
    content = f.readlines() #Store the rest in content.

    close_prices = []
    high_prices = []
    date_list = []
    
    for line in content:
        line = line.split(',')
        date_list.append(line[0])
        high_prices.append(float(line[2]))
        close_prices.append(float(line[4]))

    close_value = max(close_prices)
    high_value  = max(high_prices)

    highDate  = date_list[high_prices.index(high_value)]
    closeDate = date_list[close_prices.index(close_value)]

    info = Info()
    info.stock = stock
    info.currentClose = close_prices[0] #Current close
    info.date = date_list[0]
    info.close = close_value
    info.high  = high_value
    info.highDate = highDate
    info.closeDate = closeDate

    print stock
    print highDate
    print closeDate
    print "1% close   : ", float(close_value) - (float(close_value) * .01)
    print "2% close   : ", float(close_value) - (float(close_value) * .02)
    print "4% close   : ", float(close_value) - (float(close_value) * .04)
    print "10% close   : ", float(close_value) - (float(close_value) * .1)
    print "Last close : ", float(close_prices[0]), " - date = ", date_list[0]
    print "High close : ", float(close_value), " - date = ", closeDate
    print ""

    return info

#    
#
#       Main
#
#Get historical prices from Yahoo.
#Send stock symbols as a parameter.

stockList = []

if len(sys.argv) > 1:
    for param in sys.argv[1:]:
        stockList.append(param)
    stock = sys.argv[1]
else:
    print "Need at least one stock ticker parameter."
    sys.exit()

#print stockList

now = datetime.datetime.now()
current = now
#print now.strftime("%Y-%m-%d %H:%M")

#Yahoo apparently starts months from 0, so subtract 1 from here to get the right values.
d = now.month - 1
e = now.day
f = now.year

now = now-datetime.timedelta(days=60) #Look a number of days back.  Change this to be a parameter later.

a = now.month - 1
b = now.day
c = now.year

#Get the stock prices for each of the quotes in the command line.
infoList = []
length = len(stockList)
i = 0
while i < length:
    infoList.append(getStockPrices(a,b,c,d,e,f,stockList[i]))
    i = i + 1

MakeHTMLTable(a,b,c,d,e,f,infoList)
MakeHTMLList(a,b,c,d,e,f,infoList)

print now.strftime("%Y-%m-%d %H:%M")
