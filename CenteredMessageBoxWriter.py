from getopt import getopt
from statistics import variance
import sys
import os


class TooLongException(RuntimeError):
    pass


class UnbalancedException(RuntimeError):
    pass


class Line:
    def __init__(self, size, content=""):
        self.content = content
        self.size = size

    def add_word(self, word):
        if len(self.content) + len(word) + 1 > self.size:
            raise TooLongException(f"Line can only be {self.size} characters long")

        if self.content != "":
            self.content += " "
        
        self.content += word

    def finalize(self):
        empty_space = self.size - len(self.content)

        if empty_space % 2 != 0:
            raise UnbalancedException(f"Line with content '{self.content}' and length {len(self.content)} is unbalanced")

        spaces = (empty_space // 2) * " "

        self.content = spaces + self.content + spaces

    def copy(self):
        return Line(self.size, self.content)


class Box:
    def __init__(self, line_size, box_size, word_amount, lines):
        self.line_size = line_size
        self.box_size = box_size
        self.lines = lines
        self.word_amount = word_amount

    def add_word(self, word):
        self.curr_line.add_word(word)
        self.word_amount += 1

    def finalize_curr_line(self):
        self.curr_line.finalize()

    def copy(self):
        return Box(self.line_size, self.box_size, self.word_amount, [line.copy() for line in self.lines])

    def add_line(self):
        if len(self.lines) == self.box_size:
            raise TooLongException("Adding new line would exceed box's size")

        self.lines.append(Line(self.line_size))
        
    @property
    def curr_line(self):
        return self.lines[-1] if self.lines else None

    def __str__(self):
        s = ""
        for line in self.lines:
            s += f"\"{line.content}\"\n"
        return s

    def __repr__(self):
        return self.__str__()


def next_word(next_index, words):
    return words[next_index]

def find_valid_boxes(line_size, box_size, words):
    box = Box(line_size, box_size, 0, [])
    valid_boxes = {box}

    finished_boxes = set()
    new_valid_boxes = set()
    remove_boxes = set()

    while valid_boxes:
        for box in valid_boxes:
            remove_boxes.add(box)

            try:
                box.add_line()
            except TooLongException:
                continue

            candidate_boxes = determine_candidate_boxes(box)
            balanced_candidates = determine_balanced_boxes(candidate_boxes)

            for balanced in balanced_candidates:
                if balanced.word_amount == len(words):
                    finished_boxes.add(balanced)
                else:
                    new_valid_boxes.add(balanced)

        for box in remove_boxes:
            valid_boxes.remove(box)

        remove_boxes = set()

        for box in new_valid_boxes:
            valid_boxes.add(box)

        new_valid_boxes = set()

    return finished_boxes

def determine_candidate_boxes(box):
    candidate_boxes = set()
    new_box = box.copy()

    while new_box.word_amount != len(words):
        try:
            new_box.add_word(next_word(new_box.word_amount, words))
        except TooLongException:
            break
        else:
            candidate_boxes.add(new_box)
            new_box = new_box.copy()

    return candidate_boxes

def determine_balanced_boxes(candidate_boxes):
    balanced_candidates = set()

    for candidate in candidate_boxes:
        try:
            candidate.finalize_curr_line()
        except UnbalancedException:
            continue
        else:
            balanced_candidates.add(candidate)

    return balanced_candidates

def get_string_for_box(box):
    return str(box) + f"\n'{''.join([line.content for line in box.lines])}'" + "\n\n" + "-" * 20 + "\n"

def save_box(box, file):
    string = get_string_for_box(box)
    if not file:
        print(string)
    else:
        file.write(string)

def save_boxes(boxes):
    for box in boxes:
        save_box(box, file)

def space_rating(box):
    return "".join([line.content for line in box.lines]).count(" ")

def var_rating(box):
    non_spaces_per_line = [len(l) for l in [s.content.replace(" ", "") for s in box.lines]]
    return variance(non_spaces_per_line)

def determine_best_boxes(boxes, rating):
    best_val = rating(min(boxes, key=rating))
    return {box for box in boxes if rating(box) == best_val}


if __name__ == "__main__":
    opts, _ = getopt(sys.argv[1:], "bef:")

    file = None
    filename = None
    filter_best = False
    
    line_size, box_size = (18, 8)
    for option, value in opts:
        if option == "-e":
            line_size, box_size = (26, 10)
        elif option == "-f":
            path_to_script = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(path_to_script, value)
            file = open(filename, "a")
        elif option == "-b":
            filter_best = True

    while True:
        try:
            text = input("Text for box: ")
            words = text.split(" ")
            finished_boxes = find_valid_boxes(line_size, box_size, words)

            if not finished_boxes:
                print("No valid boxes were found")
            else:
                if filter_best:
                    finished_boxes = determine_best_boxes(finished_boxes, var_rating)

                save_boxes(finished_boxes)
                if file:
                    print(f"Wrote {len(finished_boxes)} box(es) to file '{file.name}'")

                if file:
                    file.close()
                    file = open(filename, "a")
        except KeyboardInterrupt:
            break

    if file:
        file.close()
