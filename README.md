Lets see whats gonna happen here
Not finished yet, please don't use it at the moment 


# Bot for trading
Because im a kinda lazy guy when it comes to invest and search for the best place to park your money.
On top of that I wanted to gain some experience in developing a Bot and setting up server and other resources for that.

## Legal Advice
This Repository is not an Investment strategy or something similar. It is only a training and learning project to level 
up my personal undeerstanding on setting up servers and building autonomous bots to make my life easier

### For a productive work you need a broker with an API Connection that lets you buy and sell!!

In case you don't have an idea what to use, I personally used the Alpaca API for buy, sell, etc. You can also use the 
program for other Brokers, but may have to adapt the API Connection file and how often you can call the API in a 
minute before it gives you an error 
Alpaca also gives you the possibility to experience with some kind of papter money for free. 

### Techstack

For techstack I decided for a quick start to use python, I know maybe not the fastest solution, but for sure a fast and
easy way to implement a prototype. On top I also wanted to train my python skills. 
In a near future, in case I have some time left, you will maybe find a reworked version in another language thats maybe 
a bit faster.

### How is it working?
For the start im focusing on the very fast buy and sell, so you don`t have a logic for buying single Shares and holding
them for a longer period of time, maybe I will implement that later on. 
The idea of that method is to take a lot more of small changes in the value and don't try to go on larger ammounts. Like 
we buy when the share drops about 0.5% and sell it instantly when we are around 0.5% in profit. 

### Requierments
To start the program you need to install python with the alpaca trade api and the python dotenv extension in advance. 
You can fulfill this requirement with the following command with your terminal 
COMMAND COMMAND COMMAND
You will also need an Alpaca Account and your key + secret and replace the dummy text in the .env file. please make sure
you never post your API Key and other confidential data.
Is everything installed you can now just start the program.
You can also find a dockerfile that does this whole kind of setup for you. Just install Docker and run the following 
commands in your terminal. 
COMMAND COMMAND COMMAND 

### Individualisation
In the config.py file you can find all of the possible configurations, maybe a graphical interface will be added later, 
the SYMBOL variable is for setting the share name that you wanna trade. The QTY variable sets the amount of shares the 
program will buy. In the future you will also find options to set "whole amount" or something similar or some kind of 
percentage of your portfolio.

### Further ideas and future features


