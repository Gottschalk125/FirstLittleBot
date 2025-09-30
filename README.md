Lets see whats gonna happen here
Not finished yet, please don't use it at the moment 

# Trading Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents
- [Overview](#overview)
- [Legal Advice](#legal-advice)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Docker](#docker)
- [Individualisation](#individualisation)
- [Future Features](#future-features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview
Because I'm a kinda lazy guy when it comes to investing and searching for the best place to park your money, I built this bot.  
On top of that, I wanted to gain experience in bot development and server setup.  
This project is a playground for learning and experimenting with automated trading.

## Legal Advice
_This repository is not an investment strategy or financial advice. It's for training and learning purposes only._  
**For productive use, you need a broker with an API connection that lets you buy and sell!**  
I personally used the Alpaca API, which also offers paper trading for free.  
If you use another broker, you may need to adapt the API connection and respect their rate limits.

## Tech Stack
- Python (quick and easy for prototyping)
- Alpaca Trade API
- python-dotenv
- Docker

## Installation

First, install the required Python packages:

```bash
pip install alpaca-trade-api python-dotenv
```

## Configuration
Edit the .env file and add your Alpaca API key and secret. 
**Never share your API key or other confidential data!**

## Usage
Start the bot with:

```bash
python main.py
```

## Docker
If you prefer using Docker, build and run the container with:

```bash
docker build -t trading-bot .
docker run --env-file .env trading-bot
```

## Individualisation
All configuration options are in config.py. Set the SYMBOL variable for the share you want to trade, and QTY for the 
amount. More options (like "whole amount" or portfolio percentage) may be added in the future. A graphical interface 
might also come later.

## How does it work?
For now, the bot focuses on fast buy and sell actions. No long-term holding logic yet—maybe later. The idea: catch lots 
of small price changes. Example: buy when the share drops ~0.5%, sell when you're ~0.5% in profit.

## Future Features
- GUI for configuration
- Support for more brokers
- Advanced trading strategies
- More flexible position sizing

## Contributing
Pull requests are welcome!
Feeln free to open issues or sugggest improvments/features.

## License
This project is licensed under the MIT License.

## Contact
Either Contact me via GitHub or email, will be added later on
