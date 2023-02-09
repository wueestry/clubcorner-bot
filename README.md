# clubcorner-bot

The clubcorner-bot fetches all available games without a referee from clubcorner and sends a message via telegram if a new game is available

**Installation**:
1. clone the repo

2. Telegram:
  - After opening an account on Telegram, in the search bar at the top search for “BotFather”
  - Click on the ‘BotFather’ (first result) and type `/newbot`
  - Give a unique name to your bot. After naming it, Botfather will ask for its username. Then also give a unique name BUT remember the username of your bot must end with the bot, like my_bot, hellobot etc.
  - After giving a unique name and if it gets accepted you will get a message. Save the access token

3. Edit the file app/keys.json. Add your login data for clubcorner in "email" and "clubcorner" (password). Add the access token previously generated to "telegram_token". Finally add the chat id where you have added the bot to in "telegram_chat_id"

4. Build the docker container by running `docker build -t "clubcorner:latest" .` form inside the clubcorner-bot folder. Finally run the container by running `docker run -d clubcorner`. The bot will now retreive new games every 5 minutes.
