from .core import VERSION, devcmd
from .converters import *
from .paginators import *
del discord, commands

def get_version():
    from .core import VERSION
    if VERSION.startswith('BETA'):
        try:
            import subprocess
            p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                VERSION += out.decode('utf-8').strip()
            p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            if out:
                VERSION += '+g' + out.decode('utf-8').strip()
        except Exception:
            pass
    return VERSION

async def setup(bot):
    await bot.add_cog(devcmd(bot))