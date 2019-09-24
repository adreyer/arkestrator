from django.test import TestCase
from oembed.core import replace

class OEmbedTests(TestCase):
    noembed = r"This is text that should not match any regex."
    end = r"There is this great video at %s"
    start = r"%s is a video that I like."
    middle = r"There is a movie here: %s and I really like it."
    trailing_comma = r"This is great %s, but it might not work."
    trailing_period = r"I like this video, located at %s."

    locs = ["http://www.viddler.com/explore/SYSTM/videos/49/",
            "http://www.slideshare.net/hues/easter-plants",
            "http://www.scribd.com/doc/28452730/Easter-Cards",
            "http://screenr.com/gzS",
            "http://www.5min.com/Video/How-to-Decorate-Easter-Eggs-with-Decoupage-142076462",
            "http://www.howcast.com/videos/328008-How-To-Marble-Easter-Eggs",
            "http://my.opera.com/nirvanka/albums/showpic.dml?album=519866&picture=7173711",
            "http://img20.yfrog.com/i/dy6.jpg/",
            "http://tweetphoto.com/8069529",
            "http://www.flickr.com/photos/jaimewalsh/4489497178/",
            "http://twitpic.com/1cm8us",
            "http://imgur.com/6pLoN",
            "http://twitgoo.com/1p94",
            "http://www.23hq.com/Greetingdesignstudio/photo/5464607",
            "http://www.youtube.com/watch?v=Zk7dDekYej0",
            "http://www.veoh.com/browse/videos/category/educational/watch/v7054535EZGFJqyX",
            "http://www.justin.tv/venom24",
            "http://qik.com/video/1445889",
            "http://revision3.com/diggnation/2005-10-06",
            "http://www.dailymotion.com/video/xcss6b_big-cat-easter_animals",
            "http://www.collegehumor.com/video:1682246",
            "http://www.twitvid.com/BC0BA",
            "http://www.break.com/usercontent/2006/11/18/the-evil-easter-bunny-184789",
            "http://vids.myspace.com/index.cfm?fuseaction=vids.individual&videoid=103920940",
            "http://www.metacafe.com/watch/2372088/easter_eggs/",
            "http://blip.tv/file/770127",
            "http://video.google.com/videoplay?docid=2320995867449957036",
            "http://www.revver.com/video/1574939/easter-bunny-house/",
            "http://video.yahoo.com/watch/4530253/12135472",
            "http://www.viddler.com/explore/cheezburger/videos/379/",
            "http://www.liveleak.com/view?i=d91_1239548947",
            "http://www.hulu.com/watch/23349/nova-secrets-of-lost-empires-ii-easter-island",
            "http://movieclips.com/watch/jaws_1975/youre_gonna_need_a_bigger_boat/",
            "http://crackle.com/c/How_To/How_to_Make_Ukraine_Easter_Eggs/2262274",
            "http://www.fancast.com/tv/Saturday-Night-Live/10009/1083396482/Easter-Album/videos",
            "http://www.funnyordie.com/videos/040dac4eff/easter-eggs",
            "http://vimeo.com/10429123",
            "http://www.ted.com/talks/robert_ballard_on_exploring_the_oceans.html",
            "http://www.thedailyshow.com/watch/tue-february-29-2000/headlines---leap-impact",
            "http://www.colbertnation.com/the-colbert-report-videos/181772/march-28-2006/intro---3-28-06",
            "http://www.traileraddict.com/trailer/easter-parade/trailer",
            "http://www.lala.com/#album/432627041169206995/Rihanna/Rated_R",
            "http://www.amazon.com/gp/product/B001EJMS6K/ref=s9_simh_gw_p200_i1?pf_rd_m=ATVPDKIKX0DER",
            "http://animoto.com/s/oH9VwgjOU9hpbgYXNDwLNQ",
            "http://xkcd.com/726/"]

    def get_oembed(self, url):
        try:
            return replace('%s' % url)
        except Exception as e:
            self.fail("URL: %s failed for this reason: %s" % (url, str(e)))

    def testNoEmbed(self):
        self.assertEqual(
            replace(self.noembed),
            self.noembed
        )

    def testEnd(self):
        for loc in self.locs:
            embed =  self.get_oembed(loc)

            if not embed or embed == loc:
                self.fail("URL: %s did not produce an embed object" % loc)

            for text in (self.end, self.start, self.middle, self.trailing_comma, self.trailing_period):
                self.assertEqual(
                    replace(text % loc),
                    text % embed
                )

    def testManySameEmbeds(self):
        loc = self.locs[1]
        embed =  self.get_oembed(loc)

        text = " ".join([self.middle % loc] * 100)
        resp = " ".join([self.middle % embed] * 100)
        self.assertEqual(replace(text), resp)