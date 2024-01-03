def leetscrape_question():
    import argparse

    from .GenerateCodeStub import GenerateCodeStub
    from .question import GetQuestion

    parser = argparse.ArgumentParser(
        description="Run this script to generate a code stub for the given question or pass --list to list all questions."
    )
    parser.add_argument(
        "--qid",
        metavar="Question ID",
        type=int,
        help="Enter a Leetcode question ID",
        required=True,
    )
    parser.add_argument(
        "--titleSlug",
        metavar="Title Slug",
        type=str,
        help="Enter a Leetcode question's title slug",
        required=False,
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="Output directory",
        type=str,
        help="Enter the path to the output directory",
        required=False,
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all questions without generating code stub",
        required=False,
    )
    parser.add_argument(
        "--list-output",
        "-lo",
        metavar="Output file name for list of questions",
        help="Specify the output file name. Only works when --list is specified.",
        required=False,
    )

    args = parser.parse_args()
    if args.list:
        df = GetQuestion.fetch_all_questions_id_and_stub()
        if args.list_output:
            # Save the DataFrame to the specified file
            df.to_csv(args.list_output)
            print(f"DataFrame saved to {args.list_output}")
        else:
            # Print the DataFrame to the console
            print(df.to_string())
    else:
        if not (args.qid or args.titleSlug):
            parser.error("At least one of qid or titleSlug need to be specified.")
        if args.qid:
            fcs = GenerateCodeStub(qid=args.qid)
        else:
            fcs = GenerateCodeStub(titleSlug=args.titleSlug)
        fcs.generate_code_stub_and_tests(
            directory=args.output if args.output else ".",
        )


def leetupload_solution():
    import argparse

    from sqlalchemy import create_engine

    from .ExtractSolutions import extract, upload_solutions

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
        "-dB",
        "--database_string",
        metavar="sqlAlchemy database string",
        type=str,
        help="Enter sqlAlchemy database string",
        required=False,
    )
    parser.add_argument(
        "--solution_file",
        metavar="Solution File",
        type=str,
        help="Enter the path to the solution file",
        required=False,
    )

    args = parser.parse_args()
    if not args.qid or not args.solution_file or not args.database_string:
        parser.error("QID, Database String, and Solution file need to be passed.")
    engine = create_engine(args.database_string, echo=False)
    solutions = extract(args.solution_file)
    upload_solutions(engine, args.qid, solutions)
