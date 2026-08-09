# hack club quotes!

-> project by @qwikster and @parkingTurkeys for Horions Polaris!

-> demo / app: https://quotes.qwik.top/

there are many wise words and pieces of inspiration being shared around Hack Club.
you may in fact be aware of our lord and saviour Zachary Lackary already! in his words,
"i want to cheese". such voluminous tidbits only come around once in a hackillion eons.

we designed this quote database to track for the next such beacon of inspiration!
unfortunately.... not all beacons are meant to be followed (_woah! it's our theme!_).
come with us as, under the guise of an abhorrently designed python project, we show you
just how deep the sages under our feet can reach for a tiny bit of comedy!

## what.

in all seriousness, #out-of-context was taken down a few months ago (literally 1984) due to lack of moderation and general abusezz1. Hopefully a more quote-focused infrastructure could serve better for the same general bits of text!

## ...and what's to stop this being taken down too?

each quote view has a chance to vote it up or down. if it drops too low, it's deleted, and if that trend continues the user that submitted it won't be able to continue submitting!!

## features!

- hack club oidc for identification
- proper error messages? in a hack club app? *kinda*
- it's written by full time human halucinogenerators instead of computer ones!
- you can put the full trust warranted of a 15 hour hackathon project into your prod db!

## development

to run the `hc-quotes` backend locally, you'll need both `python` and `uv` installed, and a way to serve the app (like caddy)!

clone the repo:
```sh
git clone https://qwikster/hc-quotes
cd hc-quotes
```
install the project:
```sh
uv venv
source .venv/bin/activate[.fish]
uv sync
```
set up your .env:
```sh
cp .env.example .env
```
then add your app details from https://auth.hackclub.com and turn on/off devmode!
```sh
hc-quotes
```
and set up the dependency with whatever manager you like!

by default, you'll be able to access this at http://127.0.0.1:1984 !

## Contributing
  you're welcome to submit PRs at any time! sloppy prs will be rejected on sight! fun!

## AI
  generative AI or large language models were NOT used to generate code in this project.

  consequently, ai was only and will only be used for research and debugging!!.

< this is where the useful readme ends ! >

## endpoint documentation

> [!WARNING]
> this stuff is ancient, mostly only here for posterities' sake: PLEASE read the code :pf:

# /root: GET /quotes:

- random quotes (list)
  - static HTML file that renders like 20 random quotes, served as a list of objects

# GET /quote/{id}: 1 html file:

- JINJA2 TEMPLATES
- <p>{{ title }}</p>
- link to profile: https://hackclub.enterprise.slack.com/team/SLACK_ID
  - (use `nickname` from oidc)

# POST /create: HTML form

- session linked to oauth (auto) (cookie)
- quote text, slack id of sender or anon

# POST /vote?up=true: buttons

- up: upvote, down: downvote
- if hit -2 downvotes it is deleted
- account banned if >50% of quotes are deleted (after 3 exist)

# OPTIONAL LATER: GET /user/{id} (or /user/my)

- includes session token
- returns profile info and all quotes from user or submitted by user

# OPTIONAL LATER: GET /search?q=etc

- probably dont do this sob
