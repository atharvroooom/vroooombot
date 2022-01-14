import requests as rq
import discord
import json
import os
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

client = discord.Client()

def metapull(book):
  title = ""
  for s in book:
    if s == " ":
      title += "+"
    else:
        title += s

  response = rq.get(f"https://www.googleapis.com/books/v1/volumes?q={title}")
  meta= json.loads(response.text)

  title = meta['items'][0]['volumeInfo']['title']
  
  authors = ', '.join(meta['items'][0]['volumeInfo']['authors'])
  
  publisher = meta['items'][0]['volumeInfo']['publisher'] + " in " + meta['items'][0]['volumeInfo']['publishedDate']
  
  description = meta['items'][0]['volumeInfo']['description']
  
  isbn = "ISBN 10: " + meta['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'] + ", ISBN 13: " + meta['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
  
  categories = ", ".join(meta['items'][0]['volumeInfo']['categories'])

  try:
    rating = meta['items'][0]['volumeInfo']['averageRating']
  except:
    rating = "Not Available"

  book_data = "Title: " + title + '\nAuthors: ' + authors + "\nPublisher: " + publisher + "\n" + isbn + "\nCategories: " + str(categories) + "\nRating: " + str(rating) + "\nDescription: " + description
  
  return book_data


def coverpull(cover):
  title = ""
  for s in cover:
    if s == " ":
      title += "+"
    else:
        title += s

  response = rq.get(f"https://www.googleapis.com/books/v1/volumes?q={title}")
  meta = json.loads(response.text)
  cimg = meta['items'][0]['volumeInfo']['imageLinks']['thumbnail']

  return cimg


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("%hiya!"):
    await message.channel.send("I'm here!")
  if message.content.startswith("-metafetch"): 
    book = message.content[5:]
    book_data = metapull(book)
    await message.channel.send(book_data[:1999])
  if message.content.startswith("-cover"):
    cover = message.content[5:]
    cimg = coverpull(cover)
    await message.channel.send(cimg[:1999])

keep_alive()
client.run(my_secret)
