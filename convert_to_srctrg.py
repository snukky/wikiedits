import argparse


def convert_to_srctrg(inp, src, trg):
    bad_words = ('### comment:', '### contributor:', '### id:', '### page:', '### timestamp:', '###')
    i = 0
    for line in inp:
        if line.isspace():
            continue
        if line.startswith(bad_words, 0):
            continue
        if i % 2 == 0:
            src.write(line)
        else:
            trg.write(line)
        i = i + 1


def parse_user_args():
    parser = argparse.ArgumentParser(
        description="converts to src and trg files from m2 file ",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("input",
                        help="input file to be processed. must be in the m2 format")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_user_args()
    inp = open(args.input)
    src = open(args.input.strip('.edits') + ".src", 'w')
    trg = open(args.input.strip('.edits') + ".trg", 'w')
    convert_to_srctrg(inp, src, trg)
