import hashlib
import secrets
from datetime import UTC, datetime, timedelta

import httpx
import jwt
from fastapi import Cookie, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from quotes.config import config, templates
from quotes.dbutil import DB, ID, USER
from quotes.models.session import Session as SessionModel
from quotes.models.user import User

router = APIRouter()
_jwks_client = jwt.PyJWKClient("https://auth.hackclub.com/oauth/discovery/keys")

def authfail(request: Request, error: str):
    print(f"FAILURE::: {error}")
    return templates.TemplateResponse(
        request = request,
        name = "401.html",
        status_code = 401,
        context = { "message": error }
    )

@router.get("/login")
def login():
    state = secrets.token_urlsafe(24)
    redir = RedirectResponse(url = f"https://auth.hackclub.com/oauth/authorize?client_id={config().hca_id}&redirect_uri={config().hca_uri}%2Fcallback&response_type=code&scope=openid+profile+slack_id+email&state={state}")
    redir.set_cookie(
        "oidc_state", state,
        max_age = 600, httponly = True,
        secure = config().devmode, samesite = "lax",
    )
    return redir

@router.get("/callback")
def callback(
    request: Request, response: Response, db: DB, code: str | None, state: str | None,
    oidc_state: str | None = Cookie(default = None, alias = "oidc_state")
):
    if code is None or state is None:
        return authfail(request, "missing code or state from HCA")
    if oidc_state is None or state != oidc_state:
        return authfail(request, "state does not match!!")

    token_resp = httpx.post(
        "https://auth.hackclub.com/oauth/token",
        json={
            "client_id": config().hca_id,
            "client_secret": config().hca_secret,
            "redirect_uri": f"{config().hca_uri}/callback",
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    if token_resp.status_code != 200:
        return authfail(request, "token exchange failed")
    print(token_resp.json())

    id_token = token_resp.json().get("id_token")
    if id_token is None:
        return authfail(request, "no token from HCA")

    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(id_token)
        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=config().hca_id,
            issuer="https://auth.hackclub.com",
        )
    except jwt.PyJWTError as e:
        print(e)
        return authfail(request, "got invalid token from HCA")

    hca_ident = claims["sub"]
    slack_id = claims.get("slack_id")
    email = claims.get("email")
    nickname = claims.get("nickname") or claims.get("name") or slack_id

    if slack_id is None or email is None:
        return authfail(request, "missing required fields")

    user = db.query(User).filter(User.hca_ident == hca_ident).first()
    if user is None:
        user = User(
            hca_ident=hca_ident,
            slack_id=slack_id,
            email=email,
            nickname=nickname,
        )
        db.add(user)
        db.flush()

    if user.banned:
        return authfail(request, "you are banned! contact @qwik if you think this might be a mistake")

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    session_row = SessionModel(
        token_hash=token_hash,
        user_id=user.id,
        expires_at=datetime.now(UTC) + timedelta(weeks=2),
    )
    db.add(session_row)
    db.commit()

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="token",
        value=raw_token,
        httponly=True,
        secure=not config().devmode,
        samesite="lax",
        max_age=int(timedelta(weeks=2).total_seconds()),
    )
    response.delete_cookie("oidc_state", httponly = True, secure = config().devmode, samesite = "lax")
    return response

@router.get("/logout")
def logout(response: Response):
    response = RedirectResponse(url = "/")
    response.delete_cookie("token", httponly=True, secure=not config().devmode, samesite="lax")
    return response

@router.get("/me")
def profile(request: Request, db: DB, user: USER) -> dict:
    return {
        "name": user.nickname,
        "ratio": (user.nuked_quotes / user.total_quotes) * 100
    }
