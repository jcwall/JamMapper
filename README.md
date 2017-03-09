# [JamMapper](http://ec2-54-174-141-180.compute-1.amazonaws.com:8105/) - Website is live!

Discover live music recommendations in your area! A recommendation engine embedded in a web app, JamMapper provides the latest upcoming shows in Denver, Boulder and Aspen.

### Why JamMapper?

The music recommendation industry for studio and album tracks is highly saturated with incredible, highly-tuned products that are built upon billions of data points. People everywhere use platforms such as Spotify, Apple, Pandora and the radio to receive music in a format that is built upon their previous music consumption. In other words, what you listen to today impacts what you hear tomorrow, popularized in such formats as Spotify's Discover Weekly playlist. However, I believe these formats either under-represent or pollute your music tastes. People consume music in a variety of ways for a variety of reasons, and it's incredibly difficult to distill what matters. Examples of noise include:

* environmental - your Mother listening to Michael Buble's Christmas album on repeat results in recommendations for Wham! Christmas songs (who's complaining?)
* historical - musical tastes from 5 years ago don't quite match up to today's exquisite taste
* different music for different moods - you like to listen to Nicki Minaj when you're working out but prefer a romantic acoustic mood for a live show

Furthermore, shows are a nuisance to research because you have to manually look at each venue's website, crawling through a list of lineups you either don't care about or aren't familiar with. Spotify has some functionality in this area, but it's congested with the above issues along with a lack of visualization for the venue.

### But Why Male Models?

JamMapper provides a platform for live music lovers to discover upcoming shows that fit their exact request. About a month ago Santana was announced at Red Rocks, an amazing venue in Colorado. My Dad has been listening to Santana for decades and I was quickly indoctrinated to the Latin rock god's jams as a young boy. However, the upcoming show sold out within minutes and we were out of luck. Using JamMapper, I was able search for recommendations based on Santana on the spot.

![](/screenshots/title_santana.png)

![](/screenshots/recs_santana.png)

![](/screenshots/tom_petty.png)

![](/screenshots/red_rocks.png)

As you can see from the screenshots above, JamMapper allows you to go from an initial artist request to recommendations, event information and finally venue information. This can be of incredible value for fans who are really captivated by a certain sector of a local scene, i.e. a subset of EDM in the local Denver scene.

### Work Flow

JamMapper was created through the following workflow:

![](/screenshots/tech.png)

Broken down, I used the Spotify and Eventful APIs to build a database of over 20,000 artists including all the upcoming live acts in select venues. This database was built over a couple days using mongoDB, and then filtered through the scikit-learn library in Python, before finally being pickled and formatted for output on an Amazon Web Services instance using Flask. Python was the underlying framework for all the ancillary services and the scripts can be found in the backend folder.

### Summary

The above framework illustrates the process from concept to creation of JamMapper. Special thanks goes to my fearless scrum master Erich Wellinger and Galvanize classmate/HTML whisperer Steve Iannaccone.

### TL;DR Just give me the website
[JamMapper](http://ec2-54-174-141-180.compute-1.amazonaws.com:8105/)
