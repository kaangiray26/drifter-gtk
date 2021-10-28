# Drifter

`Drifter` is a simple yet complete and useful Reddit application for desktop using GTK. It is not intended to replace the Reddit web application but to offer a more friendly approach for using Reddit.

<p align="center">
  <img alt="ss1" src="https://raw.githubusercontent.com/f34rl00/drifter/master/screenshots/v1_dark.png?token=ACWGFV4IHIHUGNZVYUNF2H3BMAZT4" width="45%">
&nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="ss2" src="https://raw.githubusercontent.com/f34rl00/drifter/master/screenshots/subs.png?token=ACWGFV2RPY4TM2EBG2FUYC3BMAZT6" width="45%">
</p>

<!-- ![Screenshot 1](https://raw.githubusercontent.com/f34rl00/drifter/master/screenshots/v1_dark.png?token=ACWGFV4IHIHUGNZVYUNF2H3BMAZT4)
![Screenshot 2](https://raw.githubusercontent.com/f34rl00/drifter/master/screenshots/subs.png?token=ACWGFV2RPY4TM2EBG2FUYC3BMAZT6)
-->

## Features
hmmmm, I'll definitely add some features in the future...

## Why?
I dunno, why not?

## Installation
The application will be available on Flathub in the future. Until then, you can go through the following instructions:

```
# Clone the repo:
git clone https://github.com/f34rl00/drifter.git

# Install required modules
pip install -r requirements.txt

# Create praw.ini
touch praw.ini # or any color you like, I don't know?

# Write the following and your fill it up with your credentials inside `praw.ini`
[auth]
username      = <username>
password      = <password>
client_id     = <client_id>
client_secret = <client_secret>
user_agent    = User-Agent: linux:com.%(username)s.drifter:v1.0 (by /u/%(username)s)
```
