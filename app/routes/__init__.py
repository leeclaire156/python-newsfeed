# The .home syntax directs the program to find the module (aka single file) named 'home' in the current directory
# Then we import the bp object from it, but we rename it 'home'
from .home import bp as home
from .dashboard import bp as dashboard