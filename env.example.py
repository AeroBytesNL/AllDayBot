class secure:
    DATABASE_HOST = str
    DATABASE_USER = str
    DATABASE_NAME = str
    DATABASE_PASSWORD = str
    BOT_TOKEN = str
    OPENAI_API_KEY = str
    MINECRAFT_DOMAIN = str
    MINECRAFT_RCON_PORT = int
    MINECRAFT_RCON_PW = str
    
class env_variable:
    GUILD_ID = int
    V_CHANNEL_ONE = int
    V_CHANNEL_TWO = int
    V_CHANNEL_THREE = int
    V_CHANNEL_FOUR = int

    ADJE_LOG_CHANNEL_ID = int
    DEV_KELVIN_ID = int
    TECH_NEWS_ID = int
    DEBUG_CHANNEL_ID = int
    BAN_LOG = int
    MODMAIL_ID = int
    KOOP_VERKOOP_ID = int

class Role_ids:
    rocket_league = int
    ADMIN = int
    MODERATOR = int
    
class Channel:
    TECH_SUPPORT = int
    ALLDAYBOT = int
    STEL_JEZELF_VOOR = int
    BUMP = int
    BLACKLISTMODLOG = int
    GENERAL = int
    BUY_SELL_FORUM = int
    KLAAGMUUR = int

class birthday_cog:
    BIRTHDAY_EMBED_CHANNEL_ID = int

class Minecraft:
    MINECRAFT_DOMAIN = str
    MINECRAFT_RCON_PW = str
    MC_SERVER_PORTS = dir
    
class Management_roles:
    OPRICHTER_ID = int
    ADMINISTRATOR = int
    MODERATOR = int
    SERVER_DEVELOPER = int

class Ntfy:
    TOPIC_BOT = str
 
class AntiBot:
    ANTI_BOT_ROLE_ID = int