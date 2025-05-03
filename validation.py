import json  # For parsing and handling JSON strings

def validate_json_fields(json_string):
    """
    Validates and scores the extracted fields from the LLM's JSON output.

    This function parses a JSON string, calculates a confidence score for each field,
    and returns a new dictionary containing both the value and its confidence score.

    Confidence is estimated based on the string length of each field (as a proxy for quality).

    Parameters:
        json_string (str): The JSON string returned by the LLM.

    Returns:
        dict: A dictionary with structure:
            {
                "Field Name": {
                    "value": "<actual value>",
                    "confidence": 0.75
                },
                ...
            }
        OR
        {
            "error": "Invalid JSON format"
        } if parsing fails.
    """

    # Try to parse the input JSON string into a Python dictionary
    try:
        data = json.loads(json_string)
    except:
        # Return an error message if JSON is malformed
        return {"error": "Invalid JSON format"}

    # Function to score confidence for each field based on value length
    def score_field(value):
        # Heuristic: longer values tend to be more meaningful and complete
        return round(len(value.strip()) / 20.0, 2) if isinstance(value, str) else 0.8

    result = {}

    # For each key-value pair in the original JSON,
    # store both the value and its calculated confidence score
    for k, v in data.items():
        result[k] = {
            "value": v,
            "confidence": score_field(v)
        }

    # Return the enriched result
    return result