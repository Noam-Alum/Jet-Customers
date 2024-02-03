#!/usr/bin/env python3
# lpi_linux.py - Prepare for the LPI 010-160 certification with a practice exam sourced from dumps
#
# Powered by Python 3
# Written by Noam Alum
#
# GitHub: https://github.com/Noam-Alum/lpi_010_160_exam/
# © Ncode. All rights reserved
# Visit ncode.codes for more scripts like this :)

### IMPORTS
import json
import requests
import random

### get json
def fetch_data():
    url = "https://ncode.codes/files/lpi/lpi_questions.json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        exit()
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        exit()

    return data

def main():
    data = fetch_data()

    # Randomize the order of questions
    random.shuffle(data)

    correct_answers = 0
    answers_review = ""

    q_count=1
    for question in data:
        print(f"\n{q_count} | {question['question']}\n")

        q_answers = question['answer']
        options = []
        answers = []

        print("Options:\n")
        for i, option in enumerate(question['options'], start=1):
            options.append(i)
            print(f"{i}) {option}")
            if option in q_answers:
                answers.append(i)

        choices = []

        while len(choices) < len(answers):
            choice = input("> ")
            while not choice.isdigit() or int(choice) < 0 or int(choice) > len(options) or choice in choices:
                choice = input("> ")

            choices.append(int(choice))

        if all(c in choices for c in answers):
            correct_answers += 1
        else:
            answers_review += (
                f"\n-------------------\n{q_count} | {question['question']}\n\nAnswer:\n"
                + "\n".join(str(answer) for answer in q_answers)
                + "\n"
            )

        print("\n######################")
        q_count+=1

    score = (correct_answers / len(data)) * 100
    print(f"You got: {score}!\n######################\nReview:{answers_review}")

if __name__ == "__main__":
    main()
