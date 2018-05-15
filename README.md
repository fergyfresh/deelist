# deelist [Link to deployed skill](https://www.amazon.com/Self-dee-list/dp/B07CVS2T1Q/ref=sr_1_2?s=digital-skills&ie=UTF8&qid=1526410612&sr=1-2)
DeeList is an Alexa skill to remove stuff from your shopping list. You can add stuff to your shopping list via the normal command `Alexa add spinach to my shopping list`, but if you want to remove stuff it tells you to use the app on your phone. Well, no more!

This project is still in it's early phases and subject to change, however it is functional and ready to use. The only few catches right now are that you have to start up your own  HTTPS web server for now, until I get it working with AWS Lambda and launch the skill for public use in the developer portal.

Features
What can this bad boy do, you ask? Well as of right now it can list your shopping list which actually doesn't work outside of the test portal because my Alexa just uses the default shopping list intent instead of my intent. It can also delete items from the shopping list. The default invocation name is `dee list` so to invoke any of the utterances you first have to say `Alexa ask dee list....`.

### Currently Implemented

```
Remove lettuce from my shopping list
What is on my shopping list
```

## Setup

How do we get this working on my Echo/Dot? The process is a bit wonky and will eventually get better once this is ported to work with AWS Lambda.

First lets get this working on your machine. Clone this repo to your server/machine:
```
$ git clone https://github.com/fergyfresh/deelist.git
```
Next, make sure you have Python 3 installed and can cd into the cloned directory to install the dependencies, you ideally want to do this in `virtualenv` as that will help keep these dependencies separate from your system installed Python 3 packages.

```
# Run this if you have virtualenv installed
$ virtualenv .venv -p python3
$ source .venv/bin/activate

# Skip to here if you don't have virtualenv installed
$ pip install -r requirements.txt
```

Once the requirements are installed we are going to go ahead and deploy this to Heroku or some similarly configured HTTPS server (note I already have the Procfile and the server init stuff setup for heroku, but be my guest to port this to other deployment options. Remember what the URL to your server that is hosting this code is, as we are going to need that later and we will call it `HTTPS_SERVER_URL` from here on out in this guide. Get it? Got it? Gooooood.

## Create the development Skill on Amazon

Open up the [Alexa Dashboard](https://developer.amazon.com/edw/home.html), click "Get Started" in the **Alexa Skills Kit** box. Then click on the "Add a New Skill" button in the top right hand corner.

Going through the various sections

### Skill Information

| Field | Value |
| ----- | ----- |
| Skill Type | Custom Interaction Model |
| Language | Select US English |
| Name | Dee List |
| Invocation Name | dee list |
| Lists Read | Yes |
| Lists Write | Yes |

### Interaction Model

This setup currently only applies to English US users. On the "Interaction Model" step, paste in the contents of `speech_assets/interactionModel.json` to the JSON editor.

### Configuration

We'll point our skill to the development server now. Select HTTPS as the endpoint type and enter the server's HTTPS_SERVER_URL (such as `https://deelist.example.com`). 


If you are using heroku, you can skip the following block of text. If you are running the server on a computer behind a firewall we'll need to expose the server via a tunnel in order for this to work. I usually use [ngrok](https://ngrok.com/) for these situations and have used it to develop this project. To start a tunnel run `ngrok http 4000` in a console window. You should then see a few URLs, one of which being a publicly accessible HTTPS link to your development server. Copy this URL, looks something like `https://[some-code].ngrok.io`.

### SSL Certificate

If using [ngrok](https://ngrok.com/) or [heroku](https://heroku.com) select the second option "My development endpoint is a subdomain of a domain that has a wildcard certificate from a certificate authority."

### Test

Scroll down to the "Service Simulator" section, the check the Skill is talking to Alexa correcty enter the word help  _"help"_ then click "Ask dee list", and you'll ideally see some resulting JSON in the Service Response box. You can then try testing phrases like_"Ask dee list to remove relish from my shopping list"_

## (Optional) Setup a Heroku instance

Setting up an instance on Heroku may be an easier option for you, and these instructions detail how to accomplish this. The following steps replace the need to setup a local server. First one must have Heroku setup on your local machine and an account associated. Visit [the CLI documentation](https://devcenter.heroku.com/articles/heroku-cli) for details on setting this up.

One must then clone the repository.

```bash
$ git clone https://github.com/fergyfresh/deelist.git
```

Next, `cd` in to deploy the code. Then, setup the Heroku server by typing the following two commands.

```bash
$ heroku create
$ git push heroku master
```

At this point, your server should by live and ready to start accepting requests at `https://[heroku_app_name].herokuapp.com` Note, that while using the free tier, you may experience timeout errors when you server has received no requests for over 30 minutes. However, you can use a service, such as [Kaffeine](http://kaffeine.herokuapp.com/) to minimize your downtime.

## Contributing

Please feel free to open an issue or PR if you've found a bug. If you're looking to implement a feature, please open an issue before creating a PR so I can review it and make sure it's something that should be added.

## License

This project is released under the GNU General Public License v3.0.
