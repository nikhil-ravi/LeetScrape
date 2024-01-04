def leetscrape_list(args, parser):
    from . import GetQuestion

    df = GetQuestion.fetch_all_questions_id_and_stub()
    if args.out:
        # Save the DataFrame to the specified file
        df.to_csv(args.out)
        print(f"DataFrame saved to {args.out}")
    else:
        # Print the DataFrame to the console
        print(df.to_string())


def leetscrape_question(args, parser):
    from . import GenerateCodeStub

    if not (args.qid or args.titleSlug):
        parser.error("At least one of qid or titleSlug need to be specified.")
        # raise ValueError("At least one of qid or titleSlug need to be specified.")
    if args.qid:
        fcs = GenerateCodeStub(qid=args.qid)
    else:
        fcs = GenerateCodeStub(titleSlug=args.titleSlug)
    fcs.generate(
        directory=args.out if args.out else ".",
    )


def leetscrape_solution(args, parser):
    import os

    from . import ExtractSolutions

    if not args.input:
        parser.error("Input needs to be specified.")
    output_dir = args.out if args.out else "."
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if input is a directory or a file
    if os.path.isdir(args.input):
        import glob
        import os

        from tqdm import tqdm

        # Get all py files in the specified directory which start with "q_"
        solution_files = glob.glob(os.path.join(args.input, "q_*.py"))
        print(f"Found {len(solution_files)} solution files in {args.input}")
        for solution_file in tqdm(solution_files):
            file_name = os.path.basename(solution_file).split(".py")[0]
            # create output file name
            output_file_name = os.path.join(output_dir, file_name + ".mdx")
            ExtractSolutions(solution_file).to_mdx(filename=output_file_name)
        print(f"Saved {len(solution_files)} solution files to {output_dir}")
    elif os.path.isfile(args.input):
        file_name = os.path.basename(args.input).split(".py")[0]
        output_file_name = os.path.join(output_dir, file_name + ".mdx")
        ExtractSolutions(args.input).to_mdx(filename=output_file_name)
        print(f"Saved solution file to {output_file_name}")


def leetscrape():
    import argparse

    parser = argparse.ArgumentParser(
        description="Run this script to interact with the leetscrape package."
    )
    subparsers = parser.add_subparsers(
        title="subcommands", dest="subcommand", help="sub-command help"
    )

    # Subcommand for listing questions
    parser_list = subparsers.add_parser(
        "list",
        help="List all questions without generating code stub",
        description="List all questions without generating code stub",
    )
    parser_list.add_argument(
        "--out",
        "-o",
        # metavar="Output file name",
        type=str,
        help="Specify the output file name",
        required=False,
    )
    parser_list.set_defaults(func=leetscrape_list)

    # Subcommand for generating code stub
    parser_question = subparsers.add_parser(
        "question",
        help="Generate a code stub for the given question",
        description="Generate a code stub for the given question",
    )
    parser_question.add_argument(
        "--qid",
        "-q",
        # metavar="Question ID",
        type=int,
        help="Enter a Leetcode question ID",
        required=False,
    )
    parser_question.add_argument(
        "--titleSlug",
        "-t",
        # metavar="Title Slug",
        type=str,
        help="Enter a Leetcode question's title slug",
        required=False,
    )
    parser_question.add_argument(
        "--out",
        "-o",
        # metavar="Output directory",
        type=str,
        help="Enter the path to the output directory",
        required=False,
    )
    parser_question.set_defaults(func=leetscrape_question)

    # Subcommand for generating mdx files for solutions
    parser_solution = subparsers.add_parser(
        "solution",
        help="Generate mdx files for solutions",
        description="Generate mdx files for solutions",
    )
    parser_solution.add_argument(
        "--input",
        "-i",
        # metavar="Solution directory",
        type=str,
        help="Enter the path to the solution directory with solution files or to a single solution file",
        required=False,
    )
    parser_solution.add_argument(
        "--out",
        "-o",
        # metavar="Output directory",
        type=str,
        help="Enter the path to the output directory to save solutions mdx files",
        required=False,
    )
    parser_solution.set_defaults(func=leetscrape_solution)

    args = parser.parse_args()
    args.func(args, parser)
