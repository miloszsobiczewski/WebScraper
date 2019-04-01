import os.path
import unittest
import webscraper.utils as ut
from web_scraper.settings import STATIC_URL


class WebScraperUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        # self.good_url = 'http://msobiczewski.pythonanywhere.com/'
        self.good_url = 'https://semantive.pl/'
        self.good_url_no_image = 'http://0.0.0.0:8000/webscraper/site/'
        self.bad_url = 'http://sdgdsgdsgdshere.com/'

    # @unittest.skip
    def test_001_get_conn(self):
        """
        Checks for site existence
        :return:
        """
        # check good site
        self.assertTrue(ut.get_conn(self.good_url))
        # check bad site
        self.assertFalse(ut.get_conn(self.bad_url))

    def test_002_make_soup(self):
        """
        Check if soup tastes good ;)
        :return:
        """
        soup = ut.make_soup(self.good_url)
        self.assertTrue(soup)

    def test_003_get_txt(self):
        """
        Check if getting any text
        :return:
        """
        text = ut.get_txt(self.good_url)
        self.assertGreater(len(text), 0)

    def test_004_save_txt(self):
        """
        check if saving file correctly
        :return:
        """
        file_path = STATIC_URL[1:] + 'api/unittests/test_text.txt'
        ut.save_txt(file_path, self.good_url)
        self.assertTrue(os.path.isfile(file_path))

    def test_005_get_images(self):
        """
        Test if retrieved links are correct
        :return:
        """
        # test collecting images
        links = ut.get_images(self.good_url)
        for link in links:
            self.assertTrue(ut.get_conn(link))

        # test with no images
        links = ut.get_images(self.good_url_no_image)
        self.assertTrue(True if len(links) == 0 else False)

    def test_006_save_img(self):
        """
        Check if images are saved
        :return:
        """
        images = ut.save_img(self.good_url, 'unittests/')[1]
        for img in images:
            self.assertTrue(os.path.isfile(img))

    @classmethod
    def tearDownClass(self):
        """
        Remove saved files
        :return:
        """
        os.system('rm static/api/unittests/*')


if __name__ == '__main__':
    unittest.main()




