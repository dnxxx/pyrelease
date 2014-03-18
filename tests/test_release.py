from datetime import timedelta

from nose.tools import assert_true, assert_false, assert_equal

from release import Release


class TestRelease(object):
    def test_repr(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal(('<Release: The.Big.Bang.Theory.S06E12.720p.HDTV.X264'
                      '-DIMENSION (PRE not fetched)>'), r.__repr__())

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        r.pre
        assert_true('TV-HD-X264' in r.__repr__())

    def test_valid_scene_release_name(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_true(r.valid_scene_release_name)

        r = Release(
            'VA-The_Hunger_Games_Catching_Fire-OST-CD-FLAC-2013-PERFECT')
        assert_true(r.valid_scene_release_name)

        r = Release('Top_Gear.20x01.720p_HDTV_x264-FoV')
        assert_true(r.valid_scene_release_name)

        r = Release('The Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_false(r.valid_scene_release_name)

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264.DIMENSION')
        assert_false(r.valid_scene_release_name)

    def test_quality(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal(r.quality, '720p')

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.720p.X264-DIMENSION')
        assert_equal(r.quality, '720p')

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.1080p.BluRay'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.quality, '1080p')

        r = Release('The.Big.Bang.Theory.S06E12.720.HDTV.X264-DIMENSION')
        assert_false(r.quality)

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.1080P.BluRay'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.quality, '1080p')

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.720P.BluRay'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.quality, '720p')

    def test_source(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal(r.source, 'HDTV')

        r = Release('The.Big.Bang.Theory.S06E12.720p.hDTv.720p.X264-DIMENSION')
        assert_equal(r.source, 'HDTV')

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.1080p.BluRay'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.source, 'BluRay')

        r = Release('The.Big.Bang.Theory.S06E12.720.dtv.X264-DIMENSION')
        assert_false(r.source)

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.1080P.Bluray'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.source, 'BluRay')

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.720P.bluray'
                    '.x264.HQ-TUSAHD'))
        assert_equal(r.source, 'BluRay')

    def test_encoding(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal(r.encoding, 'x264')

        r = Release('The.Big.Bang.Theory.S06E12.720p.hDTv.720p.x264-DIMENSION')
        assert_equal(r.encoding, 'x264')

        r = Release('The.Big.Bang.Theory.S06E12.720.dtv.264-DIMENSION')
        assert_false(r.encoding)

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.1080P.Bluray'
                    '.xvid.HQ-TUSAHD'))
        assert_equal(r.encoding, 'XviD')

        r = Release(('Man.Of.Steel.2013.DTS-HD.DTS.MULTISUBS.720P.bluray'
                    '.XviD.HQ-TUSAHD'))
        assert_equal(r.encoding, 'XviD')

    def test_safe_release_name(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal(r.safe_release_name,
                     'The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')

        r = Release('Saud_Albloushi-Bliss_Factory-(TSRB005)-WEB-2013-UKHx')
        assert_equal(r.safe_release_name,
                     'Saud_Albloushi-Bliss_Factory-TSRB005-WEB-2013-UKHx')

        r = Release('Test % Release ""')
        assert_equal(r.safe_release_name, 'Test-Release')

    def test_get_pre(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_true(timedelta(days=300) < r.pre.time_since_pre())

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264 DIMENSION')
        assert_false(r.pre.pre)

    def test_pre_ok(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_true(r.pre_ok)

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264 DIMENSION')
        assert_false(r.pre_ok)

    def test_tv_series_data(self):
        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal({'season': '06',
                      'series_name': 'The Big Bang Theory',
                      'episode': '12'}, r.tv_series_data)

        r = Release('Top_Gear.20x01.720p_HDTV_x264-FoV')
        assert_equal({'season': '20',
                      'series_name': 'Top Gear',
                      'episode': '01'}, r.tv_series_data)

    def test_series_name(self):
        r = Release('Top_Gear.20x01.720p_HDTV_x264-FoV')
        assert_equal('Top Gear', r.series_name)

        r = Release('Top_Gear.x01.720p_HDTV_x264-FoV')
        assert_false(r.series_name)

    def test_season(self):
        r = Release('Top_Gear.1x01.720p_HDTV_x264-FoV')
        assert_equal('01', r.season)

        r = Release('Top_Gear.20x01.720p_HDTV_x264-FoV')
        assert_equal('20', r.season)

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal('06', r.season)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_equal('01', r.season)

    def test_episode(self):
        r = Release('Top_Gear.1x88.720p_HDTV_x264-FoV')
        assert_equal('88', r.episode)

        r = Release('Top_Gear.20x01.720p_HDTV_x264-FoV')
        assert_equal('01', r.episode)

        r = Release('The.Big.Bang.Theory.S06E12.720p.HDTV.X264-DIMENSION')
        assert_equal('12', r.episode)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_equal('01', r.episode)

    def test_movie_release(self):
        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_true(r.movie_release)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_false(r.movie_release)

    def test_tv_release(self):
        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_false(r.tv_release)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_true(r.tv_release)

    def test_movie_data(self):
        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_equal({'movie_year': 2007, 'movie_title': 'Michael Clayton'},
                     r.movie_data)

        r = Release('Michael.Clayton.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_false(r.movie_data)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_false(r.movie_data)

    def test_movie_title(self):
        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_equal('Michael Clayton', r.movie_title)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_false(r.movie_title)

    def test_movie_year(self):
        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_equal(2007, r.movie_year)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_false(r.movie_year)

    def test_search_imdb_id(self):
        imdb_id = Release.search_imdb_id(('nfo nfo http://www.imdb.com/title'
                                          '/tt1285016/'))
        assert_equal('tt1285016', imdb_id)

        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        imdb_id = r.search_imdb_id(('nfo nfo http://www.imdb.com/title'
                                    '/tt1285016/'))
        assert_equal('tt1285016', imdb_id)

        imdb_id = Release.search_imdb_id('nfo nfo')
        assert_false(imdb_id)

    def test_imdb(self):
        r = Release('The.Big.Bang.Theory.S01E01.720p.HDTV.X264-DIMENSION')
        assert_false(r.imdb)

        r = Release('Michael.Clayton.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_false(r.imdb)

        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        assert_equal('Michael Clayton', r.imdb.title)

        r = Release('Michael.Clayton.2007.720p.iNTERNAL.BluRay.x264-MOOVEE')
        r.imdb_id = 'tt0468569'
        assert_equal('The Dark Knight', r.imdb.title)
