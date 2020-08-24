
from site_config import SiteConfig


def config(request):
    return {
        'config': SiteConfig()
    }
