from leetscrape.GetQuestionsList import GetQuestionsList
import os
import shutil


class TestGetQuestionsList:
    def test_scrape(self):
        ls = GetQuestionsList()
        ls.scrape()  # Scrape the list of questions
        os.makedirs("./tests/data/")
        ls.to_csv(directory_path="./tests/data/")  # Save
        shutil.rmtree("./tests/data/")  # Remove
