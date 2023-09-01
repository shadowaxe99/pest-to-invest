import argparse
import csv
import json
import logging
import os
import smtplib
import time

from email_manager import EmailManager
from investor import Investor, read_investors_from_csv
from templates import Templates
from tracker_manager import TrackerManager
from user_prompt import UserPrompt


def format_prompt(investor):
    return f"{investor['name']} is a {investor['type']} investor who has invested in {', '.join(investor['investments'])}."


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='The CSV file containing the investors information')
    parser.add_argument('--temperature', type=float, help='The temperature for the GPT-3 model')
    parser.add_argument('--max_tokens', type=int, help='The maximum number of tokens for the GPT-3 model')
    parser.add_argument('--mode', type=str, help='The mode for the GPT-3 model')
    parser.add_argument('--reply_speed', type=str, help='The reply speed for the GPT-3 model')
    parser.add_argument('--custom_prompt', type=str, help='A custom prompt for the GPT-3 model')
    parser.add_argument('--test', action='store_true', help='Run in test mode')

    args = parser.parse_args()

    email_manager = EmailManager()
    tracker_manager = TrackerManager()
    user_prompt = UserPrompt()

    investors = read_investors_from_csv(args.file)

    for investor in investors:
        print(f"Running - {investor.name}")
        prompt = args.custom_prompt or format_prompt(investor)
        messages = [{'role': 'system', 'content': prompt}]

        try:
            if args.reply_speed == 'slow':
                result = openai.Completion.create(
                    engine='text-davinci-002',
                    prompt=messages,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    n=1,
                    stop=None,
                    log_level='info',
                    logprobs=None,
                    echo=False,
                    logit_bias=None,
                    return_prompt=False,
                    return_sequences=True,
                    return_full_text=True
                )
            elif args.reply_speed == 'fast':
                result = openai.Completion.create(
                    engine='text-davinci-002',
                    prompt=messages,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    n=1,
                    stop=None,
                    log_level='info',
                    logprobs=None,
                    echo=False,
                    logit_bias=None,
                    return_prompt=False,
                    return_sequences=True,
                    return_full_text=True
                )
            else:
                print('Invalid reply speed specified.')
                return
        except OpenAIError as e:
            logging.error(f'WARNING: OpenAIError occurred: {str(e)}')
            continue
        except Exception as e:
            logging.error(f'WARNING: Unknown error occurred: {str(e)}')
            continue

        if not safeguard(result):
            logging.warning(f'WARNING: Not sending the email to - {investor.name}')
            failed.append({investor.name: result})
            continue

        result = openai.Completion.create(
                    engine='text-davinci-002',
                    prompt=messages,
                    temperature=args.temperature,
                    max_tokens=args.max_tokens,
                    n=1,
                    stop=None,
                    log_level='info',
                    logprobs=None,
                    echo=False,
                    logit_bias=None,
                    return_prompt=False,
                    return_sequences=True,
                    return_full_text=True
                )
                result = result.choices[0].text.strip()
        result = result.replace('[NAME]', investor.name)
        result = result.replace('[COMPANY NAME]', investor.company_name)

        investor.opens = 0
        investor.clicks = 0

        email_signature = user_prompt.get_signature()
        body = Templates.EMAIL_BODY + '\n\n' + email_signature

        if args.test:
            print(f'Test Result for {investor.name}: {result}')
        else:
            email_manager.send_email([investor.email], [], [], Templates.EMAIL_SUBJECT, body)

            # Log the email
            with open('email_log.csv', 'a') as f:
                f.write(f'{time.time()},{investor.email},{Templates.EMAIL_SUBJECT},{body}\n')

            follow_up_subject = Templates.FOLLOW_UP_SUBJECT
            follow_up_body = Templates.FOLLOW_UP_BODY

            email_manager.send_email([investor.email], [], [], follow_up_subject, follow_up_body)

            # Log the follow-up email
            with open('email_log.csv', 'a') as f:
                f.write(f'{time.time()},{investor.email},{follow_up_subject},{follow_up_body}\n')

            tracker_manager.track(investor, result)


if __name__ == '__main__':
    main()
