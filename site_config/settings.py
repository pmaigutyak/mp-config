
class SiteConfigSettings(object):

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + [
            'site_config'
        ]

    @property
    def CONTEXT_PROCESSORS(self):
        return super().CONTEXT_PROCESSORS + [
            'site_config.context_processors.config'
        ]

default = SiteConfigSettings
