import os

from TTS.Trainer.trainer.model import *
from TTS.Trainer.trainer.trainer import *

with open(os.path.join(os.path.dirname(__file__), "VERSION"), "r", encoding="utf-8") as f:
    version = f.read().strip()

__version__ = version
