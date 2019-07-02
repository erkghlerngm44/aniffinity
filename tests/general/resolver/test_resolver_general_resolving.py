"""
aniffinity general resolving tests.

Tests the ``resolver`` functions generally, without service-specific testing
(for example service aliases, individual service urls, etc).
"""

import pytest

import aniffinity


USERNAME = "foo"
FULL_SERVICE_NAME = "ANILIST"


def test_resolver_general__username_and_full_service():
    """
    Test `resolver.resolve_user` when specifying the full username/service.
    """
    res_uname, res_svc = \
        aniffinity.resolver.resolve_user(USERNAME, service=FULL_SERVICE_NAME)

    assert res_uname == USERNAME
    assert res_svc == FULL_SERVICE_NAME


def test_resolver_general__service_colon_username():
    """
    Test `resolver.resolve_user` when specifying `service:username`.
    """
    res_uname, res_svc = \
        aniffinity.resolver.resolve_user("{}:{}".format(FULL_SERVICE_NAME, USERNAME))

    assert res_uname == USERNAME
    assert res_svc == FULL_SERVICE_NAME


def test_resolver_general__service_slash_username():
    """
    Test `resolver.resolve_user` when specifying `service/username`.
    """
    res_uname, res_svc = \
        aniffinity.resolver.resolve_user("{}/{}".format(FULL_SERVICE_NAME, USERNAME))

    assert res_uname == USERNAME
    assert res_svc == FULL_SERVICE_NAME


def test_resolver_general__tuple():
    """
    Test `resolver.resolve_user` when specifying username/service as tuple.
    """
    user_tuple = (USERNAME, FULL_SERVICE_NAME)

    res_uname, res_svc = \
        aniffinity.resolver.resolve_user(user_tuple)

    assert res_uname == USERNAME
    assert res_svc == FULL_SERVICE_NAME


def test_resolver__resolve_and_call():
    """
    Test `resolver.resolve_and_call` calls the relevant endpoint.
    """
    # Create our own service so that we don't have to make any URL calls,
    # or have to monkeypatch anything for this test.
    fake_service_name = "BAZ"
    endpoint_response = "called"

    aniffinity.endpoints.SERVICES[fake_service_name] = {
        "aliases": set(),
        "url_regex": r"eegreuijgjerjgengjerigkegeperouguherkg",
        "endpoint": lambda _: endpoint_response
    }

    resp = aniffinity.resolver.resolve_and_call(USERNAME,
                                                service=fake_service_name)

    assert resp == endpoint_response

    # Tidy up so we don't have a fake endpoint floating
    # around for the other tests...
    del aniffinity.endpoints.SERVICES[fake_service_name]


def test_resolver_general__exception_invalid_service_name():
    """
    Test `resolver.resolve_user` when specifying an invalid service name.
    """
    with pytest.raises(aniffinity.exceptions.InvalidUserError) as excinfo:
        aniffinity.resolver.resolve_user(USERNAME, service="FOOBAR")

    assert "invalid service name" in str(excinfo.value).lower()


def test_resolver_general__exception_invalid_service_url():
    """
    Test `resolver.resolve_user` when specifying an invalid service URL.
    """
    with pytest.raises(aniffinity.exceptions.InvalidUserError) as excinfo:
        aniffinity.resolver.resolve_user("https://www.google.com")

    assert "invalid service url" in str(excinfo.value).lower()


def test_resolver_general__assume_default_service():
    """
    Test `resolver.resolve_user` when only a username specified.

    This should just assume the default service and work with that.
    """
    # This wrapper should be removed when/if `DEFAULT_SERVICE`
    # becomes supported behaviour.
    with pytest.warns(Warning) as warninfo:
        res_uname, res_svc = \
            aniffinity.resolver.resolve_user(USERNAME)

    assert len(warninfo) == 1
    assert "no service has been specified, so assuming" \
           in warninfo[0].message.args[0].lower()

    assert res_uname == USERNAME
    assert res_svc == aniffinity.const.DEFAULT_SERVICE


# Aliases and URL testing will happen in the service-specific tests.
