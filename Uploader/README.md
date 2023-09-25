<h1>FAQ ?</h1>
<br>
<h3>How to edit config.py</h3>

<p> Here is sample edited config.py for deploy to Locally/VPS. copy and past and edit with your variables</p>
<p> Go To sample_config.py and edit with your veriable</p>

<pre>
# sample config file 

class Config(object):

    # get a token from @BotFather
    BOT_TOKEN = "123456789:AAGuPzlgwqgHtgqmdL7yt12PRLrXFjt98Zg"
    
    # Get these values from my.telegram.org
    API_ID = 12345
    API_HASH = "uPzlgwqgHtgqmdL7yt12PRLrXFj"
    
    # No need to change
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    ADL_BOT_RQ = {}
    CHUNK_SIZE = 128
    TG_MAX_FILE_SIZE = 4194304000
    HTTP_PROXY = ""
    PROCESS_MAX_TIMEOUT = 3700
    
    # TG Ids
    LOG_CHANNEL = -1001798969594
    OWNER_ID = 1953040213
    
    # bot username without @
    BOT_USERNAME = "Url_Uploader_Z_bot"
    
    # auth users
    AUTH_USERS = [OWNER_ID, 1953040213,5144980226,874964742,839221827,5294965763]
</pre>
