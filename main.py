#import libraries
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import csv

#open csv file and use dictwriter to write column headers
with open("data.csv", 'w') as file: 
    fields = ["NAME", "PRICE", "SHIPPING"]
    writer = csv.DictWriter(file, delimiter = ",", fieldnames = fields)
    writer.writeheader()

    #initialize dict for scraped data
    data = {                
        "NAME" : "NAME",
        "PRICE" : "PRICE",
        "SHIPPING" : "SHIPPING"
        }   

    search = input("What do you want to search for?\n")
    #create url
    url = f"https://www.newegg.com/global/de-en/p/pl?d={search}" 

    #retrieve total number of pages on which the items are displayed
    page = urlopen(url)
    page_html = page.read()
    page_soup = bs(page_html, "html.parser")
    pagination = page_soup.findAll("div",{"class":"list-tool-pagination"})
    total_pages = int(pagination[0].text[7])

    #loop over all the pages and scrape data
    for i in range(1,total_pages+1):
        url = f"https://www.newegg.com/global/de-en/p/pl?d={search}&page={i}"
        page = urlopen(url)
        page_html = page.read()
        page_soup = bs(page_html, "html.parser")


        containers = page_soup.findAll("div",{"class":"item-container"})

        for container in containers:
            name = container.findAll("a",{"class":"item-title"})[0]
            name = name.text

            price = container.findAll("div",{"class":"item-action"})[0]
            price = price.ul.findAll("li",{"class":"price-current"})[0].text.strip()

            shipping = container.findAll("div",{"class":"item-action"})[0]
            shipping = shipping.ul.findAll("li",{"class":"price-ship"})[0].text

            #store data in dict
            data["NAME"] = name
            data["PRICE"] = price
            data["SHIPPING"] = shipping


            print(f"NAME: {name}")
            print(f"PRICE: {price}")
            print(f"SHIPPING: {shipping}\n")
            #write the dict to the csv file using dictwriter
            writer.writerow(data) 

file.close()