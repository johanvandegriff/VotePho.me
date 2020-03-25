# VotePho.me
Vote for your favorite photo from a gallery of options!

## Try It Out!
The app is live on my personal site: [https://votephome.johanv.xyz/](https://votephome.johanv.xyz/)

## Installation
This part is mostly for me, but you might find it useful as well, especially if you want to modify the code and run it yourself.

### Testing
This is the quick and easy way to run VotePho.me locally.
```bash
git clone https://gitlab.com/johanvandegriff/VotePho.me
cd VotePho.me
python3 routes.py
```
Then visit http://127.0.0.1:5000/ in your browser to view the app.

### Deploy to Heroku
It's easy and free to deploy an app to [Heroku](https://www.heroku.com/), which makes it accessible publicly online!
1. [Sign up](https://signup.heroku.com/) with the free plan.
2. They will send you an email to verify your email address.
3. Create an app and pick a name for it.
4. There are many ways to deploy, but the simplest one is through the terminal with git and SSH. Generate an ssh key on your local machine:
```bash
mkdir ~/.ssh
ssh-keygen -b 4096 -f ~/.ssh/heroku
cat ~/.ssh/heroku.pub #this will output the key you need to copy for the next step
```
5. Add the SSH key to [your Heroku account](https://dashboard.heroku.com/account) (scroll down and click on "Add" under "SSH Keys"). Paste in the output from the previous command and click "Save Changes".
6. Run these commands to deploy the Heroku app! Replace `yourapp` with the name you put when creating the app on Heroku.
```bash
ssh-add ~/.ssh/heroku #and enter the passphrase if you set one
git clone https://gitlab.com/johanvandegriff/VotePho.me
cd VotePho.me
git remote add heroku git@heroku.com:yourapp.git
git push heroku master
```
7. Visit `votephome.herokuapp.com` or click on "Open app" from within Heroku. It's alive! Use `votephome.herokuapp.com/admin` to upload images.

### Deploy to Dokku
These instructions are for deploying to [Dokku](http://dokku.viewdocs.io/dokku/), a PaaS that you can push apps to as a git repo and it will build and manage them in docker containers.

You need:
* a domain name pointing to...
* a server running Dokku (one click install on [DigitalOcean](https://m.do.co/c/f300a2838d1d)) with...
* (optional) the [letsencrypt dokku module](https://github.com/dokku/dokku-letsencrypt) for https

More info on how I set up these pre-requisites [here](https://blog.johanv.xyz/how-i-created-johanv-xyz).

Run these commands. Replace `yoursite.com` with your actual domain name.
```bash
git clone https://gitlab.com/johanvandegriff/VotePho.me
cd VotePho.me
git remote add dokku@yoursite.com:votephome
git push dokku master
```

(optional) Enable https with letsencrypt. Again, replace `yoursite.com` with your actual domain name and `your@email.com` with your actual email.
```bash
ssh dokku@yoursite.com config:set --no-restart votephome DOKKU_LETSENCRYPT_EMAIL=your@email.com
ssh dokku@yoursite.com letsencrypt votephome
```

(optional) To make the images uploaded persistent over reboots and rebuilds:
```bash
ssh root@yoursite.com mkdir /var/lib/dokku/data/storage/votephome
ssh root@yoursite.com chmod -R 777 /var/lib/dokku/data/storage/votephome
ssh dokku@yoursite.com storage:mount votephome /var/lib/dokku/data/storage/votephome:/app/static/images
```

(optional) Increase max upload size and password protect the admin page:
```bash
ssh root@yoursite.com #the rest of the commands should be executed once you are logged in
apt install apache2-utils
htpasswd -c /var/lib/dokku/data/storage/votephome/.htpasswd admin #will prompt you for a password
su dokku #change to the dokku user so that the permissions will be correct on the file you are about to create
#create the file using cat to dump a bunch of text to a new file
cat <<EOF > /home/dokku/votephome/nginx.conf.d/upload-password.conf
client_max_body_size 100M;

location /admin {
    auth_basic "Admin Page";
    auth_basic_user_file /var/lib/dokku/data/storage/votephome/.htpasswd;

    proxy_pass  http://votephome-5000;
    http2_push_preload on;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection $http_connection;
    proxy_set_header Host $http_host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Port $server_port;
    proxy_set_header X-Request-Start $msec;
}
EOF
exit #log out of the dokku user, back to the root user
service nginx reload #reload the web server to pick up the new config file you made
```

Done! Visit `votephome.yoursite.com` to use the app. Use `votephome.yoursite.com/admin` to upload images. If you added the password, it will prompt you. The username is `admin` and the password is whatever you set it to when you ran the `htpasswd` command.

## Credit
Credit to [evac](https://github.com/evac) on Github for the [Photo-Gallery](https://github.com/evac/Photo-Gallery) repo that I modified and used for this project.