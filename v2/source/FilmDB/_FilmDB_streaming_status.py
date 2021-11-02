from bmb.v2.source.FilmDB._standard_import           import *

class _FilmDB_streaming_status:
    def Streamer( self, text):
        streamer_id = self.get( Query.SELECT_STREAMER_ID, text, single=True)
        if not streamer_id:
            raise ValueError( f"Unknown streamer: {text}")
        return streamer_id

    def JustWatchURL( self, url):
        url_id = self.select_one( 'id', 'JustWatchURL', url=url)
        if not url_id:
            self.insert( "JustWatchURL", url=url)
            url_id = self.select_one( 'id', 'JustWatchURL', url=url)
        return url_id

    def update_streaming_content( self, streamer, **kwargs):
        streamer_id  = self.Streamer( streamer)
        streamer_key = self.select_one( 'key', 'Streamer', id=streamer_id)
        found_urls   = check_JustWatch( streamer_key, **kwargs)
        new_urls     = [ url for url in found_urls if url if not self.select_one( '*', 'JustWatchState', url=self.JustWatchURL(url), streamer=streamer_id)]

        for url in new_urls:
            self.insert( 'JustWatchState',
                streamer = streamer_id,
                url      = self.JustWatchURL( url),
                added    = self.now )

        for url in found_urls:
            self.set( Query.UPDATE_CONFIRM_TIME_FOR_JWURL_AT_STREAMER, self.now, self.JustWatchURL( url), streamer_id)

        self.insert( 'JustWatchLog',
            streamer  = streamer_id,
            start_year= kwargs[ 'ymin']  if 'ymin'  in kwargs else None,
            end_year  = kwargs[ 'ymax']  if 'ymax'  in kwargs else None,
            genre     = kwargs[ 'genre'] if 'genre' in kwargs else None,
            total     = len( found_urls),
            new       = len( new_urls),
            completed = self.now )

    def identify_new_JustWatchURLs( self, VERBOSE=False):
        unknown_urls = self.get( "SELECT url from JustWatchURL WHERE film is Null")
        for url in jupyter_aware_tqdm( unknown_urls, VERBOSE=VERBOSE):
            soup        = safe_soup( url)
            tb          = soup.find( class_='title-block')
            title, year = tb.find( 'h1').text.strip(), int( tb.find( class_='text-muted').text.split( '(')[1].split(')')[0])
            self.set( "UPDATE JustwatchURL SET film=? WHERE url=?", self.Film( title, year, lookup=True), url)
