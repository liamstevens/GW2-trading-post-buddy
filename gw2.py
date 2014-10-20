import mechanize
import cookielib
import sys
import re
from Tkinter import *

#self defined find function
def find(text, pattern, start):
    """Return the index of the first occurence of pattern in text starting
    at start. Retun -1 if not found

    find(str, str, int) -> int
    """
    pattern_len = len(pattern)
    text_len = len(text)
    i = start
    while i < text_len:
        if pattern == text[i:i+pattern_len]:
            return i
        i += 1
    return -1


#searching:
def search():
    """Searches for an item in the gw2spidy database from input, returns prices of item along with viability for flipping.

    search()-> str"""
    while True:
        #Makes a browser object
        br=mechanize.Browser()

        #Sets cookies
        cj =cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        #Sets the browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        #sets refresh rate for pages
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        #Debug messages on
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)

        #Opening a site
        r= br.open('http://gw2spidy.com')
        html = r.read()


        #print the title
        print br.title()

        #print response headers
        print r.info()

        #show available forms for entering
        for f in br.forms():
            print "Form name:", f.name
            pass

        #select the first form (has index of zero)
        br.form=list(br.forms())[0]
        

        #iterating through the controls in the form
        for control in br.form.controls:
            print control
            print "type=%s, name=%s valu=%s" % (control.type, control.name, br[control.name])
        query=form.get()
        control.value=query
        response= br.submit()
        res=response.read()
        w=open('scrape_current.txt', 'w')
        w.write(res)
        w.close()
        findprice()
        return False


    
def findprice():
    f=open('scrape_current.txt', 'rU')
    source=f.read()
    source=str(source)
    f.close()
    
##################################################################################

    #sell
    sell_index=source.find('Sell Price', 0)
    sell_end_index=source.find('</td>', sell_index)
    sellprice=source[sell_index:sell_end_index]


    #Worth at least 1 gold
    if find(sellprice, 'gold', 0) != -1:
        gold_sell_index=sellprice.find('money-fragment',0)
        gold_sell_end=sellprice.find('>g<',gold_sell_index)
        gold_sell=sellprice[gold_sell_index:gold_sell_end]
        gold_sell=gold_sell.replace("gw2money", '')
        gold_sell=re.sub("\D", '', gold_sell)
        silv_sell_index=sellprice.find('money-fragment',gold_sell_end)
        silv_sell_end=sellprice.find('>s<',silv_sell_index)
        silv_sell=sellprice[silv_sell_index:silv_sell_end]
        silv_sell=silv_sell.replace("gw2money", '')
        silv_sell=re.sub("\D", '', silv_sell)
        if len(silv_sell)==0:
            silv_sell='0'
        cop_sell_index=sellprice.find('money-fragment',silv_sell_end)
        cop_sell_end=sellprice.find('>c<',cop_sell_index)
        cop_sell=sellprice[cop_sell_index:cop_sell_end]
        cop_sell=cop_sell.replace("gw2money", '')
        cop_sell=re.sub("\D", '', cop_sell)
        if len(cop_sell)==0:
            cop_sell='0'

    #Worth at least 1 silver
    elif find(sellprice, 'silver', 0) != -1:
        silv_sell_index=sellprice.find('money-fragment',0)
        silv_sell_end=sellprice.find('>s<',silv_sell_index)
        silv_sell=sellprice[silv_sell_index:silv_sell_end]
        silv_sell=silv_sell.replace("gw2money", '')
        silv_sell=re.sub("\D", '', silv_sell)
        cop_sell_index=sellprice.find('money-fragment',silv_sell_end)
        cop_sell_end=sellprice.find('>c<',cop_sell_index)
        cop_sell=sellprice[cop_sell_index:cop_sell_end]
        cop_sell=cop_sell.replace("gw2money", '')
        cop_sell=re.sub("\D", '', cop_sell)
        if len(cop_sell) == 0:
            cop_sell = '0'
        gold_sell='0'

    #Worth less than 1 silver
    else:
        cop_sell_index=sellprice.find('money-fragment',0)
        cop_sell_end=sellprice.find('>c<',cop_sell_index)
        cop_sell=sellprice[cop_sell_index:cop_sell_end]
        cop_sell=cop_sell.replace("gw2money", '')
        cop_sell=re.sub("\D", '', cop_sell)
        silv_sell='0'
        gold_sell='0'
        
#############################################################################################

    #buy
    buy_index=source.find('Buy Price', sell_end_index)
    buy_end_index=source.find('</td>', buy_index)
    buyprice=source[buy_index:buy_end_index]

    #gold
    if find(buyprice, 'gold', 0) != -1:
        gold_buy_index=buyprice.find('money-fragment',0)
        gold_buy_end=buyprice.find('>g<',gold_buy_index)
        gold_buy=buyprice[gold_buy_index:gold_buy_end]
        gold_buy=gold_buy.replace("gw2money", '')
        gold_buy=re.sub("\D", '', gold_buy)
        silv_buy_index=buyprice.find('money-fragment',gold_buy_end)
        silv_buy_end=buyprice.find('>s<',silv_buy_index)
        silv_buy=buyprice[silv_buy_index:silv_buy_end]
        silv_buy=silv_buy.replace("gw2money", '')
        silv_buy=re.sub("\D", '', silv_buy)
        if len(silv_buy) == 0:
            silv_buy ='0'
        cop_buy_index=buyprice.find('money-fragment',silv_buy_end)
        cop_buy_end=buyprice.find('>c<',cop_buy_index)
        cop_buy=buyprice[cop_buy_index:cop_buy_end]
        cop_buy=cop_buy.replace("gw2money", '')
        cop_buy=re.sub("\D", '', cop_buy)
        if len(cop_buy) == 0:
            cop_buy='0'

    #silver
    elif find(buyprice, 'silver', 0) != -1:
        silv_buy_index=buyprice.find('money-fragment',0)
        silv_buy_end=buyprice.find('>s<',silv_buy_index)
        silv_buy=buyprice[silv_buy_index:silv_buy_end]
        silv_buy=silv_buy.replace("gw2money", '')
        silv_buy=re.sub("\D", '', silv_buy)
        cop_buy_index=buyprice.find('money-fragment',silv_buy_end)
        cop_buy_end=buyprice.find('>c<',cop_buy_index)
        cop_buy=buyprice[cop_buy_index:cop_buy_end]
        cop_buy=cop_buy.replace("gw2money", '')
        cop_buy=re.sub("\D", '', cop_buy)
        if len(cop_buy) ==0:
            cop_buy='0'
        gold_buy='0'

    #copper
    else:
        cop_buy_index=buyprice.find('money-fragment',0)
        cop_buy_end=buyprice.find('>c<',cop_buy_index)
        cop_buy=buyprice[cop_buy_index:cop_buy_end]
        if len(cop_buy) != 0:
            cop_buy=cop_buy.replace("gw2money", '')
            cop_buy=re.sub("\D", '', cop_buy)
        else:
            cop_buy = '0'
        silv_buy='0'
        gold_buy='0'
        
    
    print ("Buy: "+gold_buy + 'gold, '+ silv_buy+ 'silver, ' + cop_buy+'copper.')
    print ("Sell: "+gold_sell + 'gold ' + silv_sell + 'silver ' + cop_sell+'copper.')
    
    profit = (((int(gold_sell)*10000)+(int(silv_sell)*100)+int(cop_sell))*.85)-((int(gold_buy)*10000)+(int(silv_buy)*100)+int(cop_buy))
    profit= round(profit)
    profit = int(profit)
    if profit > 0 :
        profit=str(profit)
        #better to do using cases and a class perhaps
        if len(profit) < 3:
            prof=("Profit: " + profit + 'c')
            result.config(text=prof)
            pass
        elif len(profit) == 3:
            prof=("Profit: " + profit[0] + 's' + profit [1:] + 'c')
            result.config(text=prof)
            pass
        elif len(profit) == 4:
            prof=("Profit: " + profit[0]+ profit[1] + 's' + profit [2:] + 'c')
            result.config(text=prof)
            pass
        elif len(profit) == 5:
            prof=("Profit: " + profit[0] + 'g' + profit[1]+ profit[2] + 's' + profit[3:] + 'c')
            result.config(text=prof)
            pass
        elif len(profit) == 6:
            prof=("Profit: " + profit[0]+ profit[1] + 'g' + profit[2] + profit[3] + 's' + profit[4:] +'c')
            result.config(text=prof)
            pass
            
    else:
        prof= "Item flipping not viable."
        result.config(text=prof)
    return True
    
    
##    return buyprice, sellprice
    
root = Tk()

root.title('Guild Wars 2 - Item Flipping')

label=Label(root, text='Enter item: ')
label.pack(side=LEFT)

form=Entry(root, width=20)
form.pack(side=LEFT)


calc=Button(root, bg="white", text="Check!", command=search)
calc.pack(side=LEFT)

result=Label(root, text='')
result.pack(side=LEFT)
root.mainloop()

