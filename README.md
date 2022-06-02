<div id="top"></div>
<p align="center">
  <img src="https://img.shields.io/github/contributors/dropout1337/guilded.rip.svg?style=for-the-badge"/>
  <img src="https://img.shields.io/github/forks/dropout1337/guilded.rip.svg?style=for-the-badge"/>
  <img src="https://img.shields.io/github/stars/dropout1337/guilded.rip.svg?style=for-the-badge"/>
  <img src="https://img.shields.io/github/issues/dropout1337/guilded.rip.svg?style=for-the-badge"/>
  <img src="https://img.shields.io/github/license/dropout1337/guilded.rip.svg?style=for-the-badge"/>
</p>
  
---------------------------------------
  
<br/>
<div align="center">
  <a href="https://github.com/dropout1337/guilded.rip">
    <img src="https://img.guildedcdn.com/asset/Logos/logomark/White/Guilded_Logomark_White.png?ver=3" alt="Logo" width="120" height="120">
  </a>
  
  <h2 align="center">guilded.rip</h3>

  <p align="center">
    Authenticates and signs a discord banner, because we love discord <3
    <br />
    <br />
    <a href="https://github.com/dropout1337/guilded.rip/issues">Report Bug</a>
    ·
    <a href="https://github.com/dropout1337/guilded.rip/issues">Request Feature</a>
  </p>
</div>

---------------------------------------

```
pip install -U git+https://github.com/dropout1337/guilded.rip/
```

```py
from guilded import Session, parsers

session = Session(
    proxy = None # requests dict format ({"https": "http://localhost:8080"})
)

# Login via username/password
session.login(
    username="test",
    password="test"
)

# Login via hmac_signed_session
session.token_login("0000000.0000000.00000.00000")

# Register (username)
session.register(
    register_type="username"
    username="testing123"
)

# Register (email)
session.register(
    register_type="email"
    email="testing123@gmail.com",
    full_name="johnny the 3rd",
    name="testing123",
    password="VeryInsecurePassword."
)

# Joining a guild
session.join(
    invite="invite code"
)

# Sending a message
channel_id = parsers.channel_link_to_id("https://www.guilded.gg/dropoutnekos-Falcons/groups/3ExNPxLz/channels/f3bd64c8-5b9c-4738-8bf3-419b9670826a/chat")
session.send_message(
    channel_id=channel_id,
    message="Hello world"
)

# Adding a user as a friend (or multiple)
session.add_user(["id", "id2"])

# Check if the account is email verified
session.email_verified()

# ping (keep the account online/alive)
session.ping()

# Set accoutns status
    # Online = 1
    # Idle = 2
    # Dnd = 3
    # Offline = 4

session.set_status(
    status=1
)

# Set custom status
session.set_custom_status(
    status="Hello world"
)

# Set accounts bio
session.set_bio(
    content="Hello world",
    user_id="the accounts Id" # if not specified it will try get it from the cached user
)

# Set account profile picture
session.add_profile_picture(
    url="https://example.com/super-secret-image.png"
)

```

### Contact
View my contact information on my [telegram](https://t.me/dropoutuwu/)