import requests
import json
import nextcord
import Buttons
from datetime import datetime


def get_news(select, pool):
    with open("News/tag_priority.json", "r") as file:
        priority = json.load(file)
        if priority.get("null"):
            priority[None] = priority["null"]
            del priority["null"]

    url = f"https://www.reddit.com/r/worldnews/top.json?limit={pool}&t=day"

    resp = requests.get(url, headers = {'User-agent': 'yourbot'})

    posts = resp.json()["data"]["children"]

    for i in posts:
        post = i["data"]
        tag = post["link_flair_text"]

        if not tag in priority:
            priority[tag] = 0

        post_prio = post["upvote_ratio"] * 2**priority[tag]/50
        posts[posts.index(i)]["post_prio"] = post_prio

    posts.sort(key=lambda p:p["post_prio"])
    posts.reverse()

    for i in posts[:select]:
        post = i["data"]
        yield {"link":post["url"], "flair":post["link_flair_text"], "title":post["title"]}


async def post_news(bot, ctx=None):
    now = datetime.now()
    rolle = ""
    if not ctx:
        channel = bot.get_channel(688135334277414977)
        try:
            for role in bot.get_guild(688050375747698707).roles:
                if role.name == "news":
                    rolle = role
        except AttributeError:
            pass
    else:
        channel = ctx.channel

    articles = {i["title"]:{"link":i["link"], "flair":i["flair"]} for i in get_news(10, 100)}
    articles_short = {i["title"][:100]:{"link":i["link"], "flair":i["flair"]} for i in get_news(10, 100)}
    translate = dict(zip(articles_short.keys(), articles.keys()))

    votes = {i:dict() for i in articles.keys()}
    select = Buttons.Select_article(articles_short)
    output = await channel.send(content=f"{rolle} news vom "
                                        f"{now.day}."
                                        f"{now.month}."
                                        f"{now.year}"
                                        f" ({now.hour}:{now.minute} Uhr)",
                                view=select)
    while True:
        select = Buttons.Select_article(articles_short)
        await output.edit(content=f"{rolle} news vom "
                                        f"{now.day}."
                                        f"{now.month}."
                                        f"{now.year}"
                                        f" ({now.hour}:{now.minute} Uhr)",
                          view=select)
        await select.wait()

        vote_btns = Buttons.Vote_btns(articles_short[select.choice]["flair"], votes[translate[select.choice]])
        await output.edit(content=f"\"{translate[select.choice]}\"\n{articles_short[select.choice]['link']}", view=vote_btns)
        await vote_btns.wait()