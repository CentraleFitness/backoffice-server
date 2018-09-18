from config.default import DefaultConfig


class Config(DefaultConfig):
    ALLOWED_HOSTS = ["91.121.155.83", "psyycker.fr.nf", "0.0.0.0", "127.0.0.1"]
    LOG_LEVEL = "INFO"
    DEBUG = True
