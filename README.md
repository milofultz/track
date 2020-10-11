# Daily Tracker

I wanted to have a way to track my mood and accomplishments over time, keep track of my priority for the next day, as well as a basic journaling platform that was not pretentious or leading. Seemed like a good project and I had seen a few people on merveilles.town making some fun CLI tools in this vein, so I took a swing at it.

Inspo from [lon by dstn](https://github.com/0xdstn/lon).

### Usage

##### No options:

On prompting, input:

1. Your mood on a 1-5 scale.
1. Your accomplishments for the day.When finished, leave the line blank and press enter.
1. Your most important task for the next day.
1. A 50 character or less summary of your day.
1. A longer journal entry of anything you feel is relevant.

This will save this data into a file named `.track` in your root folder, formatted like so:

```
---
20201011 (4) Spend time on programming, exercise, and work.

* Write daily tracker program
* Exercise with 1.5hr walk
* Brainstorm programming projects
* Vote in election

> Prepare for next week and resolve all open tasks

I walked farther south than I have since moving here, and I really like how quiet
the side streets are.

Been listening to vogue ball playlists all night.

```

##### With options:

* `mit` - Print last recorded most important task.
* `overview` - Print headers of all recent entries.

### Future Implementation

* Using options:
    * Return all accomplishments.
    * Show average mood over short- and long-term scale.
    * ~~Return all headers in a list.~~
    * ~~Return yesterday's MIT.~~
    * Pull up random journal entry.
* Eventually maybe turn this into some kind of simple MERN app for practice.
* Graph mood rating over time using matplotlib.
