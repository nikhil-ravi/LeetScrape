from .GenerateCodeStub import GenerateCodeStub
import argparse

parser = argparse.ArgumentParser(
    description="Run this script to generate a code stub for the given question"
)
parser.add_argument(
    "--qid",
    metavar="Question ID",
    type=int,
    help="Enter a Leetcode question ID",
    required=False,
)
parser.add_argument(
    "--titleSlug",
    metavar="Title Slug",
    type=str,
    help="Enter a Leetcode question's title slug",
    required=False,
)


def leetscrape_question():
    args = parser.parse_args()
    if not (args.qid or args.titleSlug):
        parser.error("At least one of qid or titleSlug need to be specified.")
    if args.qid:
        fcs = GenerateCodeStub(qid=args.qid)
    else:
        fcs = GenerateCodeStub(titleSlug=args.titleSlug)
    fcs.generate_code_stub_and_tests()
