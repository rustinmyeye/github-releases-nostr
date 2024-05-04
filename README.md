# Dockerized Nostr Bot for GitHub Releases
This Dockerized Nostr bot is designed to post the most recent release of a GitHub repository to Nostr and subsequently check for any new releases every hour.

## Setup
1. Clone the Repositoryand enter the directory:

```git clone https://github.com/rustinmyeye/github-releases-nostr```

```cd github-releases-nostr```

2. Change the NOSCL_PRIVATE_KEY in the dockerfile. It needs to be the hex key because nsec1 didnt seem to work for me.

3. Add your github releases page youd like to follow to the git2nostr.py file. 

4. If you want the bot to post only new releases and not the most recent existing one, dry run the bot outside of the container first. This will add the previous release to the last_release.json file, but won't post it to Nostr because the private key won't be set.
   
5. Ensure Docker is installed on your system then, build the container with:
   

``` docker build -t nostr-bot . ``` 

6. Then to start the container:

``` docker run -d --name nostr-bot nostr-bot ```
