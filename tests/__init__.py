"""malaffinity test suite"""


import os

from vcr import VCR


# Don't create new records if tests run on Travis
record_mode = "none" if os.environ.get("TRAVIS") else "once"


def before_record_response(response):
    # Scrub out the cookies from the response
    # Doesn't work when passing `Set-Cookie` to VCR's `filter_headers`
    # so has to be done manually
    if "Set-Cookie" in response["headers"]:
        del response["headers"]["Set-Cookie"]
    return response


vcr = VCR(**{
    "cassette_library_dir": "tests/cassettes",
    "record_mode": record_mode,
    "before_record_response": before_record_response,
    "decode_compressed_response": True
})
