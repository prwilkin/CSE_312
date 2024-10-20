# CSE_312

CSE 312 Project for Fall 2024

# Framework

Using Python's Flask Framework and MongoDB

# Code standards:

## Comments

Any function should have 2 comments above its declaration that:
1) states the purpose
2) explains what is returned

Functions should be clean and have comments giving cursory explanations to logic.

## Structure

### app.py

app.py should serve as a router file and only contain route paths. Functions can be written in app.py only if they are less then 10 lines. routes should call other functions to perform the work.

### /util

/util should serve as a directory for hosting files that are used in the application. If a file is used in app.py it should be within this directory.

### /tests

Write tests for the majority of functions you write, if not all. They should be located in this directory and use the python tests library. Testing is best practice and will save **A LOT** of time.

### /templates

This is a flask folder used to render frontend pages. Read the flask docs for more info.

### /statics

This is a flask folder used to render anything else, ie .js, .png, .css, etc. Read the flask docs for more info.

# GitHub

## Commits

Make comments useful, you will read others and be grateful when they are good, and angry when they aren't. Comments should be no longer then a tweet (or x?) and should give a very basic rundown on what you commited.
**Commit often and Commit a lot**

## Branches

Never work on the dev or main branches directly. Always work on a separate dev branch. 

### main

This is the branch used by the server also known as prod or production. Never touch it without discussing with the team. Ideally two people should always been working on a merge to production.

### dev

This is the main staging branch used before rolling to main. Pull/Merge this branch frequently to avoid merge conflicts.

### developer dev branches

This is where all of your work on your tasks are done. This isnt the best method but it works well enough since we are doing task branches.