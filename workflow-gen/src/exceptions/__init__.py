class PluginError(Exception):
    """
    Base class for plugin-related exceptions.
    """
    pass

class LanguageDetectionError(PluginError):
    """
    Raised when language detection fails.
    """
    pass
