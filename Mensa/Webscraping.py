import requests
from pdf2image import convert_from_path
from datetime import date, datetime, time, timedelta
import nextcord
url = "https://lerbermatt.sv-restaurant.ch/de/menuplan/"


def menuoutput(output):
    req = requests.get(url, 'html.parser').text
    weekday = date.today().weekday()
    menuselect = 1
    output = []

    if (datetime.utcnow()+timedelta(hours=2)).time() > time(hour=14, minute=30) and weekday <5:
        menuselect=2
        weekday = (date.today()+timedelta(1)).weekday()

    items = req.split(f"<div id=\"menu-plan-tab{menuselect}")[1].replace("\t", "")\
                .split(f"<div id=\"menu-plan-tab{menuselect+1}")[0]\
                .split('<div class="menu-item">')[1::]

    for item in items:
        item = item.replace("&amp;", "&")
        title = item.split('<h2 class="menu-title">')[1].split("</h2>")[0]

        desc = item.split('<p class="menu-description">')[1].split('</p>')[0]\
            .replace("<br />\n", " ")\

        label = item.split('<div class="menu-prices prices-3">')[1]\
            .replace("\t", "")\
            .split('class="menu')[1]

        if label.startswith("-provenance"):
            label = label.split('-provenance">')[1].split('</span>')[0]

        else:
            label = label.split('-labels">\n\n\n<span class="label label-')[1].split(' has-infobox">')[0]
        output.append({"title": title, "desc":desc, "label":label})

    if output[0]["label"] not in {"vegan", "vegetarian"}:
        output[0], output[1] = output[1], output[0]

    return output


async def menuweekly(output):
    req = requests.get(url, 'html.parser').text
    await output.edit("Webscraping fertig. Slicing...")

    items = []
    allelements =req.split("\"menu-item\"")[1::]
    for i in allelements:
        dic = {"title": i.split("menu-title\">")[1].split("</h2>")[0]}

        desc = i.split("menu-description\">")[1].split("</p")[0]\
            .replace("<br />", "\n")\
            .replace("inkl.", "inkl. ")\
            .replace("&amp;", "&")
        dic["desc"] = desc

        try:
            dic["label"] = i.split("menu-labels")[1].split("<p>")[1].split(":<br />")[0]
        except IndexError:
            dic["label"] = ""
        items.append(dic)
    return items


async def weeklypdf(client):
    req = requests.get(url, 'html.parser').text
    await client.change_presence(activity=nextcord.Game("downloading menu pdf...(0/2)"))

    pdf_url = "https://lerbermatt.sv-restaurant.ch" + req.split('<div class="menu-meta-nav">')[1].split('" target="_blank">')[0].split('<a href="')[1]
    pdf = requests.get(pdf_url)

    await client.change_presence(activity=nextcord.Game("downloading menu pdf...(1/2)"))

    with open("Mensa/menu.pdf", "wb") as pdffile:
        pdffile.write(pdf.content)
    await client.change_presence(activity=nextcord.Game("Download complete. converting to png...(0/2)"))

    pages = convert_from_path('Mensa/menu.pdf', 100, poppler_path=r"poppler_bin")
    await client.change_presence(activity=nextcord.Game("Download complete. converting to png... (1/2)"))

    for i in pages:
        i.save("Mensa/menu.png")

    await client.change_presence(activity=nextcord.Game("Download complete."))

    return "menu.png"