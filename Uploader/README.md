<h1>FAQ ?</h1>
<br>
<h3>How to edit config.py</h3>

<p> Here is sample edited config.py for deploy to Locally/VPS. copy and past and edit with your variables</p>
<p> Go To sample_config.py and edit with your veriable</p>

<pre>
# sample config file 

class Config(object):

    # get a token from @BotFather
    BOT_TOKEN = ""
    
    # Get these values from my.telegram.org
    API_ID = 
    API_HASH = ""
    
    # No need to change
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    ADL_BOT_RQ = {}
    CHUNK_SIZE = 128
    TG_MAX_FILE_SIZE = 4194304000
    HTTP_PROXY = ""
    PROCESS_MAX_TIMEOUT = 3700
    
    # TG Ids
    LOG_CHANNEL = 
    OWNER_ID = 
    
    # bot username without @
    BOT_USERNAME = ""
    
    # auth users
    AUTH_USERS = []
</pre>
