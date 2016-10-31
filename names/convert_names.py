import sys


names = []

def getWord(word_num, line):
    return line.split()[word_num - 1]

def main():
    with open(sys.argv[1], 'r') as name_file:
        for line in name_file:
            try:
                names.append(getWord(1, line))
            except IndexError:
                break

    for i, name in enumerate(names):
        fixed_case_name = ''
        for j, letter in enumerate(name):
            if j != 0:
                fixed_case_letter = letter.lower()
            else:
                fixed_case_letter = letter

            fixed_case_name = fixed_case_name + fixed_case_letter

        else:
            names[i] = fixed_case_name

    with open(sys.argv[1][0:-4], 'w') as fixed_names:
        for name in names:
            fixed_names.write(name)
            fixed_names.write('\n')


if __name__ == '__main__':
    main()
