#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import capitalize

from dictionary import *


def encode(ip):
    is_ipv6 = ip_is_ipv6(ip)
    decimal_octect_array = split_ip(ip, is_ipv6)
    factord_octet_array = factor_octets(decimal_octect_array, is_ipv6)
    encoded_word_array = encode_words(factord_octet_array, is_ipv6)
    haiku_text = write_haiku(encoded_word_array, is_ipv6)
    return haiku_text


def ip_is_ipv6(ip):
    if ip.find(':') != -1:
        return True
    elif ip.find('.') != -1:
        return False
    else:
        raise ValueError("Formatting error in IP address input. "
                         "Contains neither ':' or '.'")


def split_ip(ip, is_ipv6):
    if is_ipv6:
        separator = ':'
        octet_num = 8
    else:
        separator = '.'
        octet_num = 4
    # Remove newline and space characters.
    ip = ''.join(ip.split())
    octet_array = ip.split(separator)
    # Replace missing octect with 0 if IPv6 address is in abbreviated fomat.
    if len(octet_array) < octet_num:
        if is_ipv6:
            octet_missing_num = octet_num - len(octet_array)
            octet_array = pad_octets(octet_array, octet_missing_num)
        else:
            raise ValueError("Formatting error in IP address input. "
                             "IPv4 address has fewer than 4 octets.")
    # Convert IPv6 address from hex to decimal
    decimal_octect_array = []
    if is_ipv6:
        for i in range(len(octet_array)):
            decimal_octect_array.append(int(octet_array[i], 16))
    else:
        decimal_octect_array = [int(num) for num in octet_array]
    return decimal_octect_array


def pad_octets(octet_array, octet_missing_num):
    padded_octect = 0
    length = len(octet_array)
    # If the first or last octect is blank, zero them.
    if octet_array[0] == '':
        octet_array[0] = padded_octect
    if octet_array[length - 1] == '':
        octet_array[length - 1] = padded_octect
    # Check the rest of the array for blank octects and pad as needed.
    for i in range(length):
        if octet_array[i] == '':
            octet_array[i] = padded_octect
            for j in range(octet_missing_num):
                octet_array.insert(i, padded_octect)
    return octet_array


def factor_octets(octet_array, is_ipv6):
    if is_ipv6:
        divisor = 256
    else:
        divisor = 16
    factord_octet_array = []
    for i in range(len(octet_array)):
        factord_octet_array.extend([octet_array[i] / divisor,
                                    octet_array[i] % divisor])
    return factord_octet_array


def encode_words(factor_array, is_ipv6):
    key = get_key(is_ipv6)
    encoded_word_array = []
    for i in range(len(factor_array)):
        encoded_word_array.append(key[i][factor_array[i]])
    return encoded_word_array


def get_key(is_ipv6):
    # if is_ipv6:
    #     key = ['adjectives', 'nouns', 'adjectives', 'nouns', 'verbs', 'adjectives',
    #            'adjectives', 'adjectives', 'adjectives', 'adjectives', 'nouns',
    #            'adjectives', 'nouns', 'verbs', 'adjectives', 'nouns']
    # else:
    #     key = ['animalAdjectives', 'animalColors', 'animalNouns', 'animalVerbs',
    #            'natureAdjectives', 'natureNouns', 'plantNouns', 'plantVerbs']
    if is_ipv6:
        key = [adjectives, nouns, adjectives, nouns, verbs, adjectives,
               adjectives, adjectives, adjectives, adjectives, nouns,
               adjectives, nouns, verbs, adjectives, nouns]
    else:
        key = [animal_adjectives, animal_colors, animal_nouns, animal_verbs,
               nature_adjectives, nature_nouns, plant_nouns, plant_verbs]
    return key


def write_haiku(word_array, is_ipv6):
    # String to place in schema to show word slot.
    octct = 'OCTET'
    schema_results = get_schema(is_ipv6, octct)
    schema = schema_results[0]
    non_words = schema_results[1]

    # Replace each instance of 'octet' in the schema with a word from
    # the encoded word array.
    for i in range(len(word_array)):
        for j in range(len(schema)):
            if schema[j] == octct:
                schema[j] = word_array[i]
                break
    # Capitalize appropriate words.
    schema = capitalize_haiku(schema, non_words)
    haiku = ''.join(schema)
    return haiku


def get_schema(is_ipv6, octet):
    # schema = []
    new_line = '\n'
    period = '.'
    space = ' '
    non_words = [new_line, period, space]

    if is_ipv6:
        schema = [octet, octet, 'and', octet, octet, new_line, octet, octet,
                  octet, octet, octet, octet, octet, period, new_line, octet,
                  octet, octet, octet, octet, period, new_line]
    else:
        schema = ['The', octet, octet, octet, new_line, octet, 'in the',
                  octet, octet, period, new_line, octet, octet, period,
                  new_line]
    space_num = 0
    # Add spaces before words except the first word.
    for i in range(1, len(schema)):
        i = i + space_num
        insert_space = True
        # If the next entry is a nonWord, don't add a space.
        for j in range(len(non_words)):
            if schema[i] == non_words[j]:
                insert_space = False
        # If the previous entry is a newLine, don't add a space.
        if schema[i-1] == new_line:
            insert_space = False
        if insert_space:
            schema.insert(i, space)
            space_num = space_num + 1
    return [schema, non_words]


def capitalize_haiku(haiku_array, non_words):
    period = '.'
    # Always capitalize the first word.
    haiku_array[0] = capitalize(haiku_array[0])
    for i in range(1, len(haiku_array)):
        if haiku_array[i] == period:
            # If the current entry is a period then the next entry will
            # be a newLine or a space, so check two positions after and
            # capitalize that entry, so long as it's a word.
            is_word = False
            # if i+2 > len(haiku_array) or haiku_array[i+2] == '':
            if i+2 < len(haiku_array):
                is_word = True
            # for j in range(len(non_words)):
            #     if haiku_array[i+2] == non_words[j]:
            #         is_word = False
            if is_word:
                haiku_array[i+2] = capitalize(haiku_array[i+2])
    return haiku_array