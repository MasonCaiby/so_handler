# Project

I suppose there are 3 main categories all projects in my life fall into: Climbing, Data Science, and girlfriend. This one covers the last two. My girlfriend likes dogs, a lot, who has the time to search Google for a picture of a dog, everyday, then send it to their Significant Other? Ridiculously high expectations. And if you give an SO a picture of a dog, they'll want some words to go with it. If you send a standard message, they'll know you're not trying, so you have to come up with a unique thing every time. Why not a unique love poem everytime?

This is in no way an attempt to get the gf's coworkers to think I'm cool and smart and want to hire me.

### ENTER: Computers

The goal of this project was to handle my relationship for me, so I can focus on the important things in life (downgrading routes on 8a). It is an RNN that produces love poems, an image scraper, and an emailer. Everything a relationship needs- automated. 

### The Poem Generator

I used a Kaggle data set of poems, which has them labeled as different catagories (1). I then slimmed it down to Modern Love Poems (sorry Shakespear). I trained my model over a few nights, saving the weights as I went. This let me train the model at night, pause it during the day (so I could do my actual work), and pick up where I left off. Here's an example poem (trained on a subset of the words while I made sure my code actually worked):


> (simon all schuster, dance, w. suddenly a moon and sun: o would, of that days his and the to dead: me with heart animals as he to w. of brothers in france; or mother’s faces me with countless dolours; in them curtained but lights take heart not natural have out from new to for for everything the water turns north, the days go. long, later the evening star grows bright how can the daylight linger on for men to fight, still fight? and he and lying in dug-outs, all some that human and divine. by a kind in and all


I trained it on words, not characters like some text generating RNNs. I didn't really want it to come up with new words, just rearrange some of them to make something new. The model quikcly overfit on the trial run I had (1000 words), it was honestly not enough data to get a legible and unique poem. With the weights saved, I can just reload the model everyday, grab 10 random words as input and let it go.

The decesion I still need to make is how to pick those 10 words. I'm considering the caption from the instagram picture, or maybe use a word of the day and it's definition. 



### Sources

1) https://www.kaggle.com/ultrajack/modern-renaissance-poetry
