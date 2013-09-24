import feedparser
import json
import logging
import urllib
import urllib2

from .. import core
from .. import decorators

class GenericSearch(core.BotAI):

    def __init__(self, prefix=''):
        super(GenericSearch, self).__init__()
        self.prefix = prefix
        self.clear_results()

    @decorators.message_must_begin_with_attr('prefix')
    def respond(self, sender, message):
        search_prefix = 'search '
        next_prefix   = 'next'
        clear_prefix  = 'clear'

        if message.startswith(search_prefix):
            # We've been asked to search for something.
            search_string = message[len(search_prefix):]
            result = None
            try:
                self.search(search_string)
                # Return the next result immediately, otherwise the user has to
                # type in the '....next' command manually. Which is bogus.
                result = self.next_result()
            except Exception as e:
                logging.exception('Erroe fetching search result.')
                return 'Something went wrong: %s' % (str(e))

            if result == None:
                return 'No results for %s' % (search_string)
            else:
                return result

        elif message.startswith(next_prefix):
            # Grab the next result.
            result = self.next_result()
            if result == None:
                return 'No more results'
            else:
                return result

        elif message.startswith(clear_prefix):
            # Clear all results.
            self.clear_results()
            return 'Results discarded.'

        else:
            return None

    def clear_results(self):
        self.results = []
        self.index   = 0

    def next_result(self):
        if self.index >= len(self.results):
            return None
        result = self.results[self.index]
        self.index += 1
        return '%d of %d\n%s' % (self.index, len(self.results), str(result))

    def search(self, searchString):
        self.clear_results()
        self.results = self.do_actual_search(searchString)

    def do_actual_search(self, searchString):
        pass


# Google Web Searching.
#
class GoogleResult(object):

    def __init__(self, raw_result):
        self.url = raw_result['url']
        self.title_no_formatting = raw_result['titleNoFormatting']

    def __str__(self):
        return '%s %s' % (self.url, self.title_no_formatting)


class GoogleSearch(GenericSearch):
    def __str__(self):
        return 'GoogleSearch'

    def __init__(self):
        super(GoogleSearch, self).__init__(prefix='goog.')

    def do_actual_search(self, search_string):
        # Watch the IT-crowd to get this joke.
        if search_string.strip().lower() == 'google':
            raise Exception('Erroe: infinite recursion. Internets have been broken.')

        # Hit the google api.
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&'
        url += urllib.urlencode({'q': search_string})
        response = urllib2.urlopen(url)

        # Extract the results.
        data = json.loads(response.read())
        google_results = []

        raw_results = data['responseData']['results']
        for raw_result in raw_results:
            google_results.append(GoogleResult(raw_result))
        return google_results
# end of Google Web Searching.


# Youtube Searching.
#
class YoutubeResult(object):

    def __init__(self, raw_result):
        self.link = raw_result.link
        self.title = raw_result.title

    def __str__(self):
        return '%s %s' % (self.link, self.title)


class YoutubeSearch(GenericSearch):

    def __str__(self):
        return 'YoutubeSearch'

    def __init__(self):
        super(YoutubeSearch, self).__init__(prefix='yt.')

    def do_actual_search(self, searchString):
        self.clear_results()
        url = 'http://gdata.youtube.com/feeds/api/videos?'
        url += urllib.urlencode({'q': searchString})
        resp = feedparser.parse(url)
        entries = resp.entries

        results = []
        for raw_entry in entries:
            results.append(YoutubeResult(raw_entry))
        return results
# end of Youtube Searching.
