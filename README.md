# /root: GET /quotes:
- random quotes (list)
	+ static HTML file that renders like 20 random quotes, served as a list of objects

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
