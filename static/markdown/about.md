This web app aims to be a knowledge resource for the dance rhythm arcade game, Pump it Up!

You are viewing version 0.10 of this project which publicly launched on August 5th, 2021. It is scuffed in many ways - if you would like to help make thie website better , please join our [Discord](https://discord.gg/aHbZsk7j2U)!

### Understand stepcharts at a glance & Find related charts
---
[![](/static/example-chart-card.PNG)](/chart/Super+Fantasy+-+SHK+S16+arcade)

### Learn how to execute stepcharts
---
Nakakapagpabagabag S18, Iolite Sky D24

[![](/static/example-chart-detail.PNG)](/chart/Nakakapagpabagabag+-+Dasu+feat.+Kagamine+Len+S18+arcade) [![](/static/example-chart-detail-double-cropped.PNG)](/chart/Iolite+Sky+-+Doin+D24+arcade)

Work in progress: Exact foot-placement visualization

![](/static/example-choreo-superfantasy.png)

### Learn Pump it Up skills and techniques
---
View top stepcharts for various skills

[![](/static/example-skill.PNG)](/skill/Run)



### Potential future updates
---
- **Achievements and goals**: Data analysis of PIU charts can enable defining progression trees, such as a series of stepcharts with runs that get progressively longer, twistier, or faster. Achievements or titles can be defined at finer-grained resolution from Andamiro, where it can take many months between achieving consecutive titles in the official Intermediate-Advanced-Expert title track. Imagine enabling players to work towards several titles specific to your level that challenge you across different skills in pump, including specific tech, stamina, slow twisty runs, fast runs, cross-pad transitions in doubles, etc.
- **Choreography visualization**
- **Search for specific arrow patterns in stepcharts**
- **Predictive models of stage passing difficulty**: The current models do not model life gain or loss.
- **Mobile UI redesign**
- **Linking to timestamps in charts**
- **Improving javascript rendering times**: All visualizations are client-side. Very long chart sections or weak CPUs can time out
- **Fix visual bugs**: Ugly Dee D15 (now D18), very long holds in Imagination S17 and End of the World S20, and very long chart sections
- **Progress tracking**: A simple database on this web app could replace the current practice of tracking progress with cell-phone photos or Google drive spreadsheets.
- **Visualize perfect-window timing**: Currently, rolling hits are identified and automatically clustered together. Instead, if the stepchart is displayed "as-is" with perfect-window visualizations, players studying high-level charts can make their own choices on which groups of notes to execute as rolling brackets.
- **Language localization**: Korean and Spanish prioritized


### Under the hood
---
This project started in the summer of 2020 when I couldn't play pump due to the pandemic. Altogether, it has taken about 2.5 months of full-time full-stack development effort, with most of the time spent on the back-end, and only about 1.5 weeks on the front-end.

I view this project primarily as a *platform* for data-driven analysis of Pump it Up stepcharts that enables a truly broad spectrum of possibilities. The core contribution of this platform is an algorithm that annotates where your limbs (feet and hands) are positioned in physical space to perform a stepchart. For example, two single notes could be front-facing or a 180-degree twist depending on the context. In my view, solving this problem is like a tree trunk that enables a huge space of potential downstream projects and applications, including some implemented in this web app like chart clustering/recommendations and data-driven difficulty ratings, and other possibilities like improving the quality of machine-learning driven stepchart generation from music files.

How does the algorithm work? The input are .ssc files from StepP1, containing notes and timing information (huge shoutouts to that community for providing such an awesome resource!). At its core, the program uses a Dijkstra's algorithm to find the minimum-cost path through a graph, prioritizing total minimizing physical distance moved. Each node in the graph is a 'stance-action' tuple comprising positions of each limb. I found it important to use sequence reasoning and segmentation to constrain paths in the graph, for example to guarantee alternating feet in certain situations. For several types of patterns, the "correct" way to move is ambiguous and typically depends on larger contexts: these include jacks *vs* footswitches, jumping *vs* single-foot bracketing two simultaneous notes, whether to alternate feet on hold-taps. Even seemingly straightforward "rules" like "always alternate feet on a series of single notes" have important subtleties: gallop jumps appear as single notes, but due to their rhythm they are more easily executed as jumps that have "double-steps". There is no single correct way to play pump, so I focused on recommending movements that would be useful for players: how to use heel-toe at lower levels, and identifying rolling hits that can be bracketed at higher levels. 

I would estimate the algorithm as 80%-90% accurate. If you explore this web app enough, it is not hard to find strange and incorrect foot placements. Unfortunately, I suspect that the easiest way to improve the quality of stepchart information is largely manual. If you are interested in contributing towards this, the help would be greatly appreciated - the algorithm can use "foot hints" that simply label which foot should be used for each note. This means that data of foot-annotated charts produced by people like Junare could be used to improve this website's stepchart quality.

### Future development
---
This open-source hobby project was developed full-time by a single person over a few months of unemployment, but the river of life flows on. While this project has been fun and rewarding, it is infeasible for me to continue to work on this project at the same level of effort. While I will probably be happy to continue improving the project on some nights and weekends, I have no specific timeline for implementing any of the aforementioned potential updates.

The open-source nature of this project means that anyone around the world can build off of this project. I think of the v0.1 launch as handing my project over to the world. If the community gets excited about the potential of this project, it is my hope that we can realize this potential together.

If you are a developer with back-end or front-end skills and are interested in contributing or working together on this, you are very welcome to our Discord!
