# dirty_smash
Quick and dirty script for applying the "Smashing the State Machine" research that I wrote to help a project test their fixes for a race condition. 

Basically this code just slices and dices multiple requests in a way that enables them to be sent in parallel ... which opens up a world for cool vulnerabilities. 

Read more here: https://portswigger.net/research/smashing-the-state-machine

Write up about what inspired me to dive into this type of issue more: https://medium.com/@gonzo-hacks/the-fast-and-the-curious-finding-a-race-condition-in-worldcoin-621c89bfbd61

# Install
`pip install h2spacex`

# Usage 

`python run.py`

This will just make post requests using the url, token, and request body provided when prompted. 

Probably not helpful for you out of the box -- change as you see fit :) 
