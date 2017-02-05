# Cryptomarket Audioscape

This script pulls the latest trade history for a particular trading pair on from Poloniex.
It then maps those trades to audio files depending on how many standard deviations the amount is 
away from the std of the last day of trading. 

A background rain(.mp3|wav) and any number of thunder(.mp3|wav) files must be provided as source.

##Dependencies
afplay - audio player for osx
python-poloniex - https://github.com/s4w3d0ff/python-poloniex for api requests on poloniex

## Installation
Clone and run once dependencies are present

## Usage

`python rain_player.py USDT_BTC rain.mp3 light_thunder.mp3 medium_thunder.mp3 loud_thunder.mp3`
