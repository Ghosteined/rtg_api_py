from rbxm_parser import *
from typing_extensions import List, Literal
from pathlib import Path

import json
import base64

type AttachmentType = Literal["cup", "ball"]

ROOT = Path(__file__).parent
file_path = ROOT  / "items.rbxm"
rbx_file = parse_rbxm(file_path)
root = rbx_file.tree[0]