try:
    # try to import config
    import config # import config to use throughout project (easier than redefining the config in every file)
except:
    # errors on import, most likely doesn't exist but the code will handle that so we do nothing
    pass


db: 'AsyncSQLPool' # type hinting