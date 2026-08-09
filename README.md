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

  consequently, ai was only and will only be used for research and debugging!!

## endpoint documentation
> [!NOTE]
> this list does not include the template files, just callables!

> [!IMPORTANT]
> **POST** requests require an authenticated cookie with a session from Hack Club Auth. there may later come endpoints to callback in ways more friendly for automations! 

## Authentication

### GET `/login`
- *params*:
  - none!
- *returns*:
  - cookie: oidc_state
  - 302: Hack Club Auth link

### GET `/callback`
- *params*:
  - cookie: oidc_state
  - code: str from HCA
- *returns*:
  - cookie: **token**
  - 303: /

### GET `/logout`:
- *params*:
  - cookie: **token**
- *response*:
  - removes cookie
  - 303: /

### GET `/me`:
- *params*:
  - cookie: **token**
    - (simply returns 401 without this!)
- *response*:
  - json:
    - name: "user.nickname",
    - ratio: float *(deleted / total quotes)*

## Content

### GET `/quotes`:
- *params*: 
  - limit: int = 30
  - offset: int = 0
  - query: str
  - sort: str (top | bottom | new | old | random | alphabet)
- *returns*: 
```
  [
  {
    "id": str(6),
    "author": str,
    "quote": str,
    "submitter": str,
    "votes": int,
    "voted": bool (returns True if you include token and have voted or are unauthenticated)
  },
  { ... },
  ]
```
### /q/{id}
exists, but is only really used for browsers right now as it returns a templated file :( sorry

## Creation

### POST `/create`:
- *params*:
  - author: str(64)
  - quote: str(1024)
- *returns*:
  - 303: /q/{id}

### POST `/vote`:
note: votes *intentionally* cannot be retracted
- *params*:
  - id: str(6),
  - up: bool
- *returns*:
  - id: str(6)
  - votes: int
