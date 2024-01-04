import os
import shutil

from leetscrape import GetQuestionsList


class TestGetQuestionsList:
    def test_scrape(self):
        ls = GetQuestionsList()
        ls.scrape()  # Scrape the list of questions
        os.makedirs("./tests/data/")
        ls.to_csv(directory="./tests/data/")  # Save
        shutil.rmtree("./tests/data/")  # Remove
