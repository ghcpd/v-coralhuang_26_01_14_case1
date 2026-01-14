import json
import os
import sys

str_types = (str,)


# Load all lines from browser.json file
# Returns array of objects
def load():
    data = []
    try:
        # Get the directory where this script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_dir, "data", "browsers.json")
        
        with open(json_file, "r", encoding="utf-8") as file:
            json_lines = file.read()
            for line in json_lines.splitlines():
                if line.strip():  # Skip empty lines
                    data.append(json.loads(line))
    except Exception as exc:
        from log import logger
        from errors import FakeUserAgentError
        
        logger.warning(
            "Unable to find local data/json file or could not parse the contents.",
            exc_info=exc,
        )
        raise FakeUserAgentError("Could not load browser data", exc)

    if not data:
        from errors import FakeUserAgentError
        raise FakeUserAgentError("Data list is empty", data)

    if not isinstance(data, list):
        from errors import FakeUserAgentError
        raise FakeUserAgentError("Data is not a list ", data)
    
    return data
