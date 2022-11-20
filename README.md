# Devcmd

A discord.py extension for developers to help manage there bot

## Warning!

```diff
- THIS IS ONLY BEING MAINTANED ON THE LATEST VERSION OF PYTHON AND DPY
```

## Index

> <a href="https://github.com/cibere/devcmd#features">Features</a>
>
> <a href="https://github.com/cibere/devcmd#Installation">Installation</a>
>
> <a href="https://github.com/cibere/devcmd#devcmd-versions">Devcmd Versions</a>
>
> <a href="https://github.com/cibere/devcmd#notes">Extra Notes</a>
>
> <a href="https://github.com/cibere/devcmd#credits">Credits</a>

## Features

> 1.  Hide your name <br>
>     If your anything like me, you want your irl name to be hidden. devcmd will replace your name with `<my name>` if you set the `NAME` env variable to your name. Example:
>
> ```
> NAME=cibere
> ```

## Installation

> 1. Install through pip and git
>
> ```
> pip install git+https://github.com/cibere/devcmd
> ```
>
> 2. Load the extension devcmd
>
> ```
> await bot.load_extension('devcmd')
> ```

## Devcmd Versions:

> devcmd currently has two versions.
> Master which is the stable version.<br> > <a href="https://github.com/cibere/devcmd#installation">Installation Guide</a>

> Beta which is the development version.
> To install, install via git and pip as so:
>
> ```
> pip install git+https://github.com/cibere/devcmd@beta
> ```

## Notes:

> The restart and shutdown commands will call `bot.shutdown_check` (if it exists) before restarting/shutting down. If the function returns false, it will abort the action. If it returns true, it will continue with the action.

## Credits:

> cibere#6647 - everything else
>
> AmongBrown#5609 - helped with the eval command
