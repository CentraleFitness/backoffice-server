from config.default import DefaultConfig


class Config(DefaultConfig):
    ALLOWED_HOSTS.extend(["91.121.155.83", "psyycker.fr.nf"])
    LOG_LEVEL = "INFO"
    DEBUG = False
