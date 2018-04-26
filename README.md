# Project

I suppose there are 3 main categories all projects in my life fall into: Climbing, Data Science, and Girlfriend. This one covers the last two. My girlfriend likes dogs, a lot, who has the time to search Google for a picture of a dog, everyday, then send it to their Significant Other? Ridiculously high expectations. And if you give an SO a picture of a dog, they'll want some words to go with it. If you send a standard message, they'll know you're not trying, so you have to come up with a unique thing every time. Why not a unique love poem everytime?

This is in no way an attempt to get the gf's coworkers to think I'm cool, and smart, and want to hire me.

### ENTER: Computers

The goal of this project was to handle my relationship for me, so I can focus on the important things in life (downgrading routes on 8a and making cool data viz projects). It is an LSTM - RNN that produces love poems, an image scraper, and an emailer. Everything a relationship needs- automated. 

### The Poem Generator

I used a Kaggle data set of poems, which has them labeled as different catagories (1). I then slimmed it down to Modern Love Poems (sorry Shakespear). I trained my model over a few nights, on a free AWS instance, saving the weights as I went. Here's an example poem (trained on a subset of the words while I made sure my code actually worked):


> (simon all schuster, dance, w. suddenly a moon and sun: o would, of that days his and the to dead: me with heart animals as he to w. of brothers in france; or mother’s faces me with countless dolours; in them curtained but lights take heart not natural have out from new to for for everything the water turns north, the days go. long, later the evening star grows bright how can the daylight linger on for men to fight, still fight? and he and lying in dug-outs, all some that human and divine. by a kind in and all


I trained it on words, not characters like some text generating RNNs. I didn't really want it to come up with new words, just rearrange some of them to make something new. The model quikcly overfit on the trial run I had (1000 words), it was honestly not enough data to get a legible and unique poem. I trained it on AWS on all words (~10,000). With the weights saved, I can just reload the model everyday, grab 10 random words as input and let it go.

### The emailer

I used the built in MIME emailer, and connected it to a purpose built gmail account, I'm considering building a web-app for it and connecting it to a database so people can use it too, but I'm working on other things right now. If you want to use this, you can fork the repo (I'll add the weights file soon), add a .csv called 'gmail.csv' with your: ```email@gmail.com, password``` in it and you should be good to go. The email comes out as a simple html email, with the body containing the poem and the image you scrape from flickr. The if ```__name__ == __main__``` block gives an example of how to call the script, if you need it. Here's an example email (with outdated weights):

![emaile example](https://github.com/MasonCaiby/so_handler/blob/master/Screen%20Shot%202018-04-26%20at%2012.08.04%20PM.png)

** My girlfriend doesn't actually call me that... I swear

### flickr scrapper

This pulls images from flickr, and checks against other images to make sure it isn't sending the same one. A #TODO will be to add the names to a file and delete the actual image after it has been sent, so you don't have to store all the old images on your computer. It searches for certain tags you can change them in the query function. As I understand it, it searches for any of those tags, randomly but it seems to only search for the last one. I therefore randomized the order the tags are in. If you would like to search for other things, just change the tags in that function.

### main.py

This just runs everything that is needed to send the email. It currently takes ~18 seconds to run, I'd like to do some reasearch into speeding this up, probably need to figure out a better way to load the weights/model; that takes about half the time. Kinda busy right now though, so I'll have to work on that later. 

### Sources

1) https://www.kaggle.com/ultrajack/modern-renaissance-poetry
