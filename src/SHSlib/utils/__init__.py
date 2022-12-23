# Bad fix, if LCD is not used and spidev is also not installd
import sys

if "spidev" in sys.modules:
    from .LCD import LCD
