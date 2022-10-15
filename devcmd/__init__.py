from .core import VERSION, devcmd
from .utils import *

def get_version():
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

async def setup(bot):
    await bot.add_cog(devcmd(bot))