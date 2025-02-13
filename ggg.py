#!/usr/bin/env python3

import argparse
import itertools
import random
import os
import operator

def read_people(file):
    with open(file, "r") as f:
        ppl = f.readlines()
    return list(map(lambda x: x.strip(), ppl))

def read_infile(file):
    already_paired = []
    if os.path.isfile(file):
        with open(file, "r") as f:
            ofile = f.readlines()
        for line in map(lambda x: x.strip(), ofile):
            if line == "":
                break
            if line == "---":
                already_paired.append("-")
                continue
            pair = tuple(line.split(","))
            already_paired.append(pair)
    return already_paired

def output(file, already_paired, selected, extra):
    with open(file, "w") as f:
        for pair in already_paired:
            if pair == "-":
                f.write("---\n")
            else:
                f.write(f"{pair[0]},{pair[1]}\n")
        f.write("---\n")
        for pair in selected:
            f.write(f"{pair[0]},{pair[1]}\n")
        for remaining in list(extra):
            f.write(f"{remaining},none\n")

        f.write("\n\n")

        f.write("Next\n")
        for pair in selected:
            f.write(f"{pair[0]},{pair[1]}\n")
        for remaining in list(extra):
            f.write(f"Extra: {remaining}\n")

    with open(file, "r") as f:
        for line in f.readlines():
            print(line.strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="people_file")
    parser.add_argument(dest="infile")
    args = parser.parse_args()

    people = read_people(args.people_file)
    already_paired = read_infile(args.infile)
    deduped_already_paired = sorted([x for x in set(already_paired) if x != "-"], key=operator.itemgetter(0,1))
    pairs = itertools.combinations(people, 2)
    good_pairs = [p for p in pairs if p not in deduped_already_paired and (p[1],p[0]) not in deduped_already_paired]
    random.shuffle(good_pairs)
    selected_pairs = []
    for pair in good_pairs:
        if pair[0] in people and pair[1] in people:
            selected_pairs.append(pair)
            people.remove(pair[0])
            people.remove(pair[1])
    outfile = args.infile + ".RC"
    output(outfile, already_paired, selected_pairs, people)


main()
