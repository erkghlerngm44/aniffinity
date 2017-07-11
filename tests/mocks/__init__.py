import copy
import malaffinity


# dummy user's list
DUMMY_LIST = [
    {"id": 413, "score": 1},
    {"id": 849, "score": 10},
    {"id": 2189, "score": 9},
    {"id": 4181, "score": 10},
    {"id": 4224, "score": 5},
    {"id": 4382, "score": 10},
    {"id": 5680, "score": 10},
    {"id": 6547, "score": 8},
    {"id": 7311, "score": 10},
    {"id": 7791, "score": 10},
    {"id": 9253, "score": 8},
    {"id": 9617, "score": 10},
    {"id": 10087, "score": 8},
    {"id": 11111, "score": 3},
    {"id": 22789, "score": 10},
    {"id": 31904, "score": 10}
]


def mock_myanimelist_endpoint(mock_username):
    assert mock_username

    return DUMMY_LIST


def mock_mini_myanimelist_endpoint(mock_username):
    assert mock_username

    return DUMMY_LIST[:5]


def mock_stdev_zero_myanimelist_endpoint(mock_username):
    assert mock_username

    # Avoid messing up the dummylist
    new_dummy = copy.deepcopy(DUMMY_LIST)

    for entry in new_dummy:
        entry["score"] = 1

    return new_dummy


def dummy_list_to_base_scores():
    scores = {}

    for entry in DUMMY_LIST:
        scores[entry["id"]] = [entry["score"]]

    return scores


def hook_mock_endpoint_and_run_function(function, mock_endpoint):
    """
    Override `malaffinity.endpoints.myanimelist` with `mock_endpoint`
    and execute `function`, which makes use of the endpoint

    Note: If `function` fails here, any other tests succeeding it,
    that are using this endpoint will also fail, as the endpoint
    won't revert back from `mock_endpoint` to the original

    :param function: Function to run after `mock_endpoint` hooked up
    :param mock_endpoint: Mock endpoint to override the actual endpoint with
    :return: whatever `function` returns
    """

    # Create a backup of the endpoint to revert to
    _myanimelist_endpoint = malaffinity.endpoints.myanimelist

    # Override the endpoint with the mock
    malaffinity.endpoints.myanimelist = mock_endpoint

    # Run funct
    ret = function()

    # Reset
    malaffinity.endpoints.myanimelist = _myanimelist_endpoint

    # Bleh
    return ret
