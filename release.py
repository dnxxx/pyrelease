import re

from lazy import lazy


class Release(object):
    """A release"""
    def __init__(self, release_name):
        self.release_name = release_name

        self.pre_fetched = False

    def __repr__(self):
        if self.pre_fetched:
            return '<Release: {} (PRE {})>'.format(
                self.release_name, self.pre.time_since_pre_human)
        else:
            return '<Release: {} (PRE not fetched)>'.format(self.release_name)

    @lazy
    def valid_scene_release_name(self):
        m = re.match(r'^[A-Za-z0-9._()\-]+-[A-Za-z0-9_]+$', self.release_name,
                     re.I)
        if not m:
            return False

        return True

    @lazy
    def quality(self):
        m = re.search(r'[._-](720p|1080p)[._-]', self.release_name, re.I)
        if not m:
            return None

        return m.group(1).lower()

    @lazy
    def source(self):
        m = re.search(r'[._-](BluRay|HDTV)[._-]', self.release_name, re.I)
        if not m:
            return None

        source = m.group(1).lower()
        if source == 'bluray':
            source = 'BluRay'
        elif source == 'hdtv':
            source = 'HDTV'

        return source

    @lazy
    def encoding(self):
        m = re.search(r'[._-](x264|XviD)[._-]', self.release_name, re.I)
        if not m:
            return None

        encoding = m.group(1).lower()
        if encoding == 'x264':
            encoding = 'x264'
        elif encoding == 'xvid':
            encoding = 'XviD'

        return encoding

    @lazy
    def tv_series_data(self):
        """Try to match tv series name and season + episode from release
        name"""
        m = re.search(r'^(?P<series_name>.+)[._](?P<s_ep>S([0-9]{2,2})E[0-9]'
                      '{2,2}|([0-9]{1,2})x[0-9]{2,2})[._].+',
                      self.release_name)
        if not m:
            return {}

        series_name = re.sub(r'[_.]', ' ', m.group('series_name'))

        # Set season and episode
        if 'x' in m.group('s_ep'):
            m = m.group('s_ep').split('x')
            season = m[0]
            episode = m[1]
        else:
            m = re.match(r'S([0-9]+)E([0-9]+)', m.group('s_ep'))
            season = m.group(1)
            episode = m.group(2)

        # Add leading zero if needed
        if len(season) == 1:
            season = '0{}'.format(season)

        return {'series_name': series_name,
                'season': season,
                'episode': episode}

    @lazy
    def series_name(self):
        return self.tv_series_data.get('series_name')

    @lazy
    def season(self):
        return self.tv_series_data.get('season')

    @lazy
    def episode(self):
        return self.tv_series_data.get('episode')

    @lazy
    def safe_release_name(self):
        """Return a safe release name stripped from unwanted characters"""
        safe_release_name = re.sub('[^A-Za-z0-9-_.]', '-', self.release_name)
        safe_release_name = re.sub('--+', '-', safe_release_name)
        safe_release_name = re.sub('^-', '', safe_release_name)
        safe_release_name = re.sub('-$', '', safe_release_name)
        return safe_release_name

    @lazy
    def movie_release(self):
        m = re.match(('^(?!.*[._]((S[0-9]{1,4})?E[0-9]{1,4}|S[0-9]{1,4}|[0-9]'
                      '{1,4}x[0-9]{1,4}))(?!.*[._\-]XXX[._\-])'
                      '(?=.*[._]x264[._\-])'
                      '(?=.*[._](BluRay|BlueRay|HDDVD)[._\-])'
                      '(?=.*[._](720p|1080p)[._\-]).*$'), self.release_name)

        if m:
            return True
        else:
            return False

    @lazy
    def tv_release(self):
        if self.series_name and self.season and self.episode:
            return True
        else:
            return False

    @lazy
    def movie_data(self):
        if not self.movie_release:
            return {}

        m = re.search(('^(?P<movie_name>[\w._-]+)[._-]'
                       '(?P<movie_year>(19|20)[0-9]{2,2})'), self.release_name)
        if not m:
            return {}

        title = re.sub('[._-]', ' ', m.group('movie_name'))
        year = int(m.group('movie_year'))

        return {'movie_title': title, 'movie_year': year}

    @lazy
    def movie_title(self):
        return self.movie_data.get('movie_title')

    @lazy
    def movie_year(self):
        return self.movie_data.get('movie_year')

    @lazy
    def pre(self):
        """Get PRE for release"""
        from pre import Pre

        pre = Pre(self.release_name)
        pre.get_pre()

        self.pre_fetched = True

        return pre

    @lazy
    def pre_ok(self):
        return self.pre.pre

    @lazy
    def imdb(self):
        """Get IMDb data for release, set self.imdb_id to override auto match
        from movie title + year"""
        from imdbpie import Imdb
        imdb = Imdb()

        if not self.movie_release:
            return False

        imdb_id = None
        if hasattr(self, 'imdb_id'):
            imdb_id = self.imdb_id

        # Find IMDb match by title and check if year is a match
        if not imdb_id:
            for imdb_match in imdb.find_by_title(self.movie_title):
                if int(imdb_match.get('year')) == self.movie_year:
                    imdb_id = imdb_match.get('imdb_id')
                    break

        # No IMDb match could be found from title + year
        if not imdb_id:
            return False

        return imdb.find_movie_by_id(imdb_id)

    @staticmethod
    def search_imdb_id(text):
        m = re.search(r'/(tt\d+)', text)
        if not m:
            return False

        return m.group(1)
