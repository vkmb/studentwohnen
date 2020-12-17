#!/bin/zsh                                #Can be bash too

# <bitbar.title></bitbar.title>
# <bitbar.author>Mithun</bitbar.author>
# <bitbar.author.github>vkmb</bitbar.author.github>
# <bitbar.desc>Display student apartments list</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.version>1.10.1</bitbar.version>
# <bitbar.abouturl></bitbar.abouturl>

source {replace_me}/.zshrc|.bashrc          #Source preset gloable variables
python3 {replace_me}/studentwohnen.py       #Path to the downloaded studentwohnen.py file 