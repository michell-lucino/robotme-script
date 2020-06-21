#  Code to get a X Æ A-12 version of a name/word
#  Created by Michell Lucino

import string, re


alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
letters_dict = dict(enumerate(string.ascii_uppercase, 1))
vowels = ['a', 'e', 'i', 'o', 'u']
vowels_dict = {1: 'a', 2: 'e', 3: 'i', 4: 'o', 5: 'u'}


def remove_special_letters(human_name):  # Remove all special letters like á, ê, ã #
    human_name = re.sub(r"[àáâãäå]", "a", human_name.lower())
    human_name = re.sub(r"[èéêë]", "e", human_name.lower())
    human_name = re.sub(r"[ìíîï]", "i", human_name.lower())
    human_name = re.sub(r"[òóôö]", "o", human_name.lower())
    human_name = re.sub(r"[ùúûü]", "u", human_name.lower())
    human_name = re.sub(r"[ç]", "c", human_name.lower())

    return human_name # Return name without special letters


def mod(n):  # Return the absolute value of a number #
    if n < 0:
        return n * -1
    else:
        return n


def get_part_type(part):  # Return the type of the pair of letters (VV, CC, VC or CV) #
    if part[0] in vowels and part[1] in vowels:  # VV - Vowel Vowel
        return 'VV'
    elif part[0] not in vowels and part[1] not in vowels:  # CC - Consonant Consonant
        return 'CC'
    elif part[0] in vowels and part[1] not in vowels:  # VC - Vowel Consonant
        return 'VC'
    else: # CV - Consonant Vowel
        return 'CV'


def trans_letter(t):  # Transform a single letter to a "special" one #
    letters_dict = dict(enumerate(string.ascii_lowercase, 1))
    letter_number = ''

    for key, letter in letters_dict.items():
        if letter == t[0]:
            if key < 10:
                letter_number = '60' + str(key)
            else:
                letter_number = '6' + str(key)

    return chr(int(letter_number))  # ASCII codes that starts with 6 and has 4 numbers


def trans_cons_vow(t):  # Transform a pair of a consonant and vowel to a "special" letter #
    letters_dict = dict(enumerate(string.ascii_lowercase, 1))
    cons_number = ''
    vow_number = ''

    for key, letter in letters_dict.items():
        if letter == t[0]:
            if key < 10:
                cons_number = '4' + str(key)
            elif key < 20:
                cons_number = '3' + str(key)[1]
            else:
                cons_number = str(key)

    for key, vowel in vowels_dict.items():
        if vowel == t[1]:
            vow_number = str(key)

    return chr(int('0' + cons_number + vow_number))  # ASCII codes that starts with 4, 3 or 2 and has 3 numbers


def trans_vow_cons(t):  # Transform a pair of a vowel and consonant to a "special" letter #
    letters_dict = dict(enumerate(string.ascii_lowercase, 1))
    vow_number = ''
    cons_number = ''

    for key, vowel in vowels_dict.items():
        if vowel == t[0]:
            vow_number = str(key)

    for key, letter in letters_dict.items():
        if letter == t[1]:
            if key < 10:
                cons_number = '0' + str(key)
            else:
                cons_number = str(key)

    return chr(int('1' + cons_number + vow_number)) # ASCII codes that starts with 1 and has 4 numbers


def trans_vow_vow(t):  # Transform a pair of a vowel and vowel to a "special" letter #
    vow1_number = ''
    vow2_number = ''

    for key, vowel in vowels_dict.items():
        if vowel == t[0]:
            vow1_number = str(key)

        if vowel == t[1]:
            vow2_number = str(key)

    return chr(int('9' + vow1_number + vow2_number)) # ASCII codes that starts with 9 and has 3 numbers


def trans_cons_cons(t):  # Transform a pair of a consonant and consonant to a "special" letter #
    letters_dict = dict(enumerate(string.ascii_lowercase, 1))
    cons1_number = ''
    cons2_number = ''

    for key, letter in letters_dict.items():
        if letter == t[0]:
            cons1_number = str(key)

        if letter == t[1]:
            cons2_number = str(key)

    if len(cons1_number + cons2_number) == 2:  # Both consonants keys are minor than 10
        return chr(int('5' + cons1_number + cons2_number))  # ASCII codes that starts with 5 and has 3 numbers
    elif len(cons1_number) == 1 and len(cons2_number) == 2:  # Second consonant key is greater than 10 and the first isn't
        return chr(int('9' + cons2_number + cons1_number))  # ASCII codes that starts with 9 and has 4 numbers
    elif len(cons1_number) == 2 and len(cons2_number) == 1:  # First consonant key is greater than 10 and the second isn't
        return chr(int('8' + cons1_number + cons2_number))  # ASCII codes that starts with 8 and has 4 numbers
    else:  # Both consonants keys are greater than 10
        # When this happens we sum 7500 to the cons_numbers, so the ASCII codes will always be between 8510 and 10126
        return chr(int(cons1_number + cons2_number) + 7500)


def validate_letter_AE(letter):  # Validate Letter of the AE part #
    if letter.lower() in alpha:
        return False
    return True


def robotize(name):  # Robotize a given name #
    try:
        if len(name) >= 3:  # Only names with more then 3 characters #
            # Part One: The X #
            part_one = mod((88 - ord(name[0].upper())))  # Get the distance between X and the first letter of the Name
            part_one = letters_dict[part_one]  # The letter that represents the number of the distance

            # Part Two: The AE #
            strip_rest_one = name[1:].lower()  # Name without the first letter

            if len(name) == 3:  # For names with only 3 letters
                part_two = trans_letter(strip_rest_one[0])  # Transform the letter in the middle

                # Part Three: The A-12 #
                part_three = 'AX-' + str(ord(strip_rest_one[1]) - 12)  # Since it's only one letter in the end, we put an 'AX-' and the number will be the ASCII code of the last letter minus 12

            else:  # For names with more than 3 letters
                strip_rest_one = [strip_rest_one[i:i + 2] for i in range(0, len(strip_rest_one), 2)]  # Strip the rest of the name in pairs

                part_two = ''
                for p in strip_rest_one[:len(strip_rest_one) - 1]:  # Loop through all pairs, except the last one
                    # Verify the type of pair and add the special letter to 'part_two' #
                    if get_part_type(p) == 'CV':
                        part_two += trans_cons_vow(p)
                    elif get_part_type(p) == 'VV':
                        part_two += trans_vow_vow(p)
                    elif get_part_type(p) == 'VC':
                        part_two += trans_vow_cons(p)
                    else:
                        part_two += trans_cons_cons(p)

                # Part Three: The A-12 #
                if len(strip_rest_one[len(strip_rest_one) - 1]) == 1:  # if the last pair is only one letter
                    part_three = 'AX-' + str(ord(strip_rest_one[len(strip_rest_one) - 1]) - 12)  # We put an 'AX-' and the number will be the ASCII code of the last letter minus 12
                else:
                    part_three = strip_rest_one[len(strip_rest_one) - 1][0].upper() + '-' + str(
                        ord(strip_rest_one[len(strip_rest_one) - 1][1]) - 12)  # The first letter of the pair will and the number will be the ASCII code of the last letter minus 12

            return part_one + ' ' + part_two + ' ' + part_three  # Return the robotized name
    except:
        return False


def humanize(robot_name):  # Humanize a given robot name #
    letters_dict = dict(enumerate(string.ascii_lowercase, 1))
    robot_name = robot_name.split(' ')
    humanized_name = ''

    try:
        # Humanize Part One: The X #
        # Do the letter minus 64 to get the letter key of the alphabet (1 to 26), then do it minus 88 to get the original letter
        humanized_name += chr(mod((ord(robot_name[0]) - 64) - 88))

        # Humanize Part Two: The AE #
        for letter in robot_name[1]:
            if validate_letter_AE(letter):
                if len(str(ord(letter))) == 3: # ASCII code with 3 numbers

                    if str(ord(letter))[0] == '6':  # Only one letter
                        humanized_name += letters_dict[int(str(ord(letter))[1:])]
                    elif str(ord(letter))[0] == '3':  # CV
                        humanized_name += letters_dict[int('1' + str(ord(letter))[1])]  # Consonant
                        humanized_name += vowels_dict[int(str(ord(letter))[2])]  # Vowel
                    elif str(ord(letter))[0] == '4':  # CV
                        humanized_name += letters_dict[int(str(ord(letter))[1])]  # Consonant
                        humanized_name += vowels_dict[int(str(ord(letter))[2])]  # Vowel
                    elif str(ord(letter))[0] == '5':  # CC
                        humanized_name += letters_dict[int(str(ord(letter))[1])]  # Consonant
                        humanized_name += letters_dict[int(str(ord(letter))[2])]  # Consonant
                    elif str(ord(letter))[0] == '9':  # VV
                        humanized_name += vowels_dict[int(str(ord(letter))[1])]  # Vowel
                        humanized_name += vowels_dict[int(str(ord(letter))[2])]  # Vowel
                    else:  # CV
                        humanized_name += letters_dict[int(str(ord(letter))[0:2])]  # Consonant
                        humanized_name += vowels_dict[int(str(ord(letter))[2])]  # Vowel

                elif len(str(ord(letter))) == 4: # ASCII code with 4 numbers

                    if str(ord(letter))[0] == '1':  # VC
                        humanized_name += vowels_dict[int(str(ord(letter))[3])]  # Vowel
                        humanized_name += letters_dict[int(str(ord(letter))[1:3])]  # Consonant
                    elif str(ord(letter))[0:2] == '91' or str(ord(letter))[0:2] == '92':  # CC
                        humanized_name += letters_dict[int(str(ord(letter))[1:3])]  # Consonant
                        humanized_name += letters_dict[int(str(ord(letter))[3])]  # Consonant
                    elif str(ord(letter))[0:2] == '81' or str(ord(letter))[0:2] == '82':  # CC
                        humanized_name += letters_dict[int(str(ord(letter))[1:3])]  # Consonant
                        humanized_name += letters_dict[int(str(ord(letter))[3])]  # Consonant
                    else:  # CC
                        mod_letter = str(ord(letter) - 7500)
                        humanized_name += letters_dict[int(mod_letter[0:2])]  # Consonant
                        humanized_name += letters_dict[int(mod_letter[2:])]  # Consonant

            else:  # Invalid robot name #
                return False

        # Humanize Part Three: The A-12 #
        if '-' in robot_name[2]:
            part_three = robot_name[2].split("-")
            if part_three[0] == "AX":  # Only one letter
                humanized_name += chr(int(part_three[1]) + 12)
            else:  # Two letters
                humanized_name += part_three[0].lower() + chr(int(part_three[1]) + 12)
        else:  # Invalid robot name #
            return False

        return humanized_name  # Return the Humanized name
    except:
        return False


first_name = input()
first_name = remove_special_letters(first_name)

print(robotize(first_name))
print(humanize(robotize(first_name)))
