# RTG API

A Python library to make Road to Gramby's creation codes using python code, you can make anything that you can build using the standard tools (except ephemeral attachments which were not added yet).

## Installation

```bash
pip install git+https://github.com/Ghosteined/rtg_api.git
```

## Quick Start

Here is an exemple to make a 10 connector tall tower with a red colored base and blue colored tower.
```python
from rtg_api import *

# Creating a new red connector
base_part = RtgPart("Connector")
base_part.set_property("RGB", [255, 0, 0])

# Creating a new blue connector
derived_part = RtgPart("Connector")
derived_part.set_property("RGB", [0, 0, 255])

# Create a structure for the code and adding the base part
struct = Structure()
struct.add(base_part)

# Get the attachment ids for the top cup and the bottom ball
top_id = RtgPart.get_cup_id("Connector", Vector3(0, 1, 0))
bottom_id = RtgPart.get_ball_id("Connector", Vector3(0, -1, 0))

# Creating a 10 tall connector tower
current_part = base_part
for i in range(10):
    new_part = derived_part.clone()

    ball = new_part.get_attachment_from_id(bottom_id)
    cup = current_part.get_attachment_from_id(top_id)

    # Attaching the last part in the tower to the new one
    ball.attach(cup)
    current_part = new_part

# Priting the creation code
print(struct.code)
```

## Notes

Ephemeral attachments will probably be added soon !