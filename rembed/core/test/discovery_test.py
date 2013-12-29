from rembed.core import discovery

from hamcrest import assert_that, equal_to
from mock import patch, Mock
import pytest


def test_should_find_oembed_url_using_json_by_default():
    expected_url = 'http://example.com/oembed?format=json'
    assert_that(get_oembed_url(),
                equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_json_when_specified():
    expected_url = 'http://example.com/oembed?format=json'
    assert_that(get_oembed_url(format='json'),
                equal_to(('json', expected_url)))


def test_should_find_oembed_url_using_xml_when_specified():
    expected_url = 'http://example.com/oembed?format=xml'
    assert_that(get_oembed_url(format='xml'),
                equal_to(('xml', expected_url)))


def test_should_return_xml_if_json_not_present():
    expected_url = 'http://example.com/oembed?format=xml'
    assert_that(get_oembed_url(fixture='no_json_oembed.html'),
                equal_to(('xml', expected_url)))


def test_should_add_max_width_when_query_string_present():
    expected_url = 'http://example.com/oembed?format=json&maxwidth=100'
    assert_that(get_oembed_url(max_width=100),
                equal_to(('json', expected_url)))


def test_should_add_max_height_when_query_string_present():
    expected_url = 'http://example.com/oembed?format=json&maxheight=200'
    assert_that(get_oembed_url(max_height=200),
                equal_to(('json', expected_url)))


def test_should_add_max_width_and_height_when_query_string_present():
    expected_url = \
        'http://example.com/oembed?format=json&maxwidth=100&maxheight=200'
    assert_that(get_oembed_url(max_width=100, max_height=200),
                equal_to(('json', expected_url)))


def test_should_add_max_width_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxwidth=100'
    assert_that(
        get_oembed_url(fixture='no_query_string.html', max_width=100),
        equal_to(('json', expected_url)))


def test_should_add_max_height_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxheight=200'
    assert_that(
        get_oembed_url(fixture='no_query_string.html', max_height=200),
        equal_to(('json', expected_url)))


def test_should_add_max_width_and_height_when_no_query_string_present():
    expected_url = 'http://example.com/oembed?maxwidth=100&maxheight=200'
    assert_that(
        get_oembed_url(
            fixture='no_query_string.html', max_width=100, max_height=200),
        equal_to(('json', expected_url)))


def test_should_throw_error_if_href_not_present():
    with pytest.raises(discovery.REmbedDiscoveryError):
        get_oembed_url(fixture='json_oembed_no_href.html')


def test_should_throw_error_for_invalid_html():
    with pytest.raises(discovery.REmbedDiscoveryError):
        get_oembed_url(fixture='invalid.html')


def test_should_throw_error_when_invalid_format_specified():
    with pytest.raises(discovery.REmbedDiscoveryError):
        get_oembed_url(format='txt')


def test_should_throw_error_on_error_response():
    with pytest.raises(discovery.REmbedDiscoveryError):
        get_oembed_url(ok=False)


def get_oembed_url(fixture='valid_oembed.html',
                   format=None,
                   max_width=None,
                   max_height=None,
                   ok=True):
    with patch('requests.get') as mock_get:
        response = Mock()
        response.ok = ok
        response.text = open(
            'rembed/core/test/fixtures/discovery/' + fixture).read()
        mock_get.return_value = response

        result = discovery.get_oembed_url(
            'http://example.com', format, max_width, max_height)

        mock_get.assert_called_with('http://example.com')
        return result