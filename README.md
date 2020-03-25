# VotePho.me
Vote for your favorite photo from a selection!

## Usage
[View the demo here](https://votephome.johanv.xyz/)

## Installation
### Testing
This is the quick and easy way to run VotePho.me locally.
```bash
git clone https://gitlab.com/johanvandegriff/VotePho.me
cd VotePho.me
python3 routes.py
```
Then visit http://127.0.0.1:5000/ in your browser to view the app.

### Deploy
These instructions are for deploying to [Dokku](http://dokku.viewdocs.io/dokku/), a PaaS that you can push apps to as a git repo and it will build and manage them in docker containers.

#### Prerequisites
* a domain name pointing to...
* a server running Dokku (one click install on [DigitalOcean](https://m.do.co/c/f300a2838d1d)) with...
* (optional) the [letsencrypt dokku module](https://github.com/dokku/dokku-letsencrypt) for https

#### Commands
In these commands, replace `yoursite.com` with your actual domain name.
```bash
git clone https://gitlab.com/johanvandegriff/VotePho.me
cd VotePho.me
git remote add dokku@yoursite.com:votephome
git push dokku master
```

Optional steps for https. Again, replace `yoursite.com` with your actual domain name and `your@email.com` with your actual email.
```bash
ssh dokku@yoursite.com config:set --no-restart votephome DOKKU_LETSENCRYPT_EMAIL=your@email.com
ssh dokku@yoursite.com letsencrypt votephome
```