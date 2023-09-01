import argparse
import csv
import json
import logging
import os
import time
from typing import List

import openai
from email_manager import EmailManager
from templates import Templates
from user_prompt import UserPrompt

openai.api_key = "sk-xxx" # add you api key here
def format_prompt(investor):
    user_prompt = UserPrompt()
    prompt = user_prompt.get_prompt()
    prompt = prompt.replace('[NAME]', investor["Name"])
    prompt = prompt.replace('[COMPANY NAME]', investor['Company Name'])
    return prompt


def read_investors_from_csv(file):
    investors = []
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            investors.append(row)
    return investors


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='The CSV file containing the investors information')
    parser.add_argument('--temperature', type=float, help='The temperature for the GPT-3 model')
    parser.add_argument('--max_tokens', type=int, help='The maximum number of tokens for the GPT-3 model')
    parser.add_argument('--mode', type=str, help='The mode for the GPT-3 model')
    parser.add_argument('--reply_speed', type=str, help='The reply speed for the GPT-3 model')
    parser.add_argument('--custom_prompt', type=str, help='The custom prompt for the GPT-3 model')
    parser.add_argument('--test', action='store_true', help='Run in test mode')

    args = parser.parse_args()

    investors = read_investors_from_csv(args.file)

    email_manager = EmailManager()
    print("investors", investors)
    for investor in investors:
        print(f'Running - {investor["Name"]}')
        prompt = format_prompt(investor)

        try:
            result = openai.Completion.create(
                engine='text-davinci-002',
                prompt=prompt,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                n=1,
                # stop=None,
                # log_level='info',
                # logprobs=None,
                # echo=False,
                # return_prompt=False,
                # return_sequences=True,
                # return_full_text=True
            )
        except Exception as e:
            logging.error(f'Error occurred: {str(e)}')
            continue

        result = result.choices[0].text.strip()
        result = result.replace('[NAME]', investor['Name'])
        result = result.replace('[COMPANY NAME]', investor['Company Name'])
        templates = Templates()
        body = templates.format_email_body(raw_body=result)
        signature = UserPrompt.get_signature()
        body += '\n\n' + signature

        if args.test:
            print(f'Test Result for {investor["Name"]}:\n{body}')
        else:
            email_manager.send_email([investor['email']], [], [], Templates.EMAIL_SUBJECT, body)

        follow_up_subject = templates.format_follow_up_subject("Following up")
        follow_up_body = templates.get_template()
        follow_up_body = follow_up_body.replace('[NAME]', investor['Name'])
        follow_up_body += '\n\n' + signature

        if args.test:
            print(f'Test Result for Follow-up Email to {investor["Name"]}:\n{follow_up_body}')
        else:
            import datetime
            email_manager = EmailManager()
            email_manager.send_email(
                subject=follow_up_subject, 
                to=[investor['email']], 
                attachments=[],
                date=datetime.datetime.now(),
                cc=[],
                msg={
                    'To': [investor['Email']],
                    'From':[],
                    'Cc': [],
                    'Subject': follow_up_subject
                },
                body=follow_up_body)


if __name__ == '__main__':
    main()
