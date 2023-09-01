# Elysium Files

This is a program for sending personalized emails to a list of investors. It uses the GPT-3 model to generate email content based on investor information.

## Setup

1. Clone the repository:
   ```
   git clone <repository_url>
   ```
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key by following the instructions in the [OpenAI documentation](https://docs.openai.com/)
4. Prepare a CSV file with the investor information. The file should have the following columns: Name, Company Name, and Email.
5. Customize the email templates in the `templates.py` file.
6. Customize the email signature in the `email_signature.txt` file.

## Usage

To run the program, use the following command:

```shell
python3 main.py --file <csv_file> --temperature <temperature> --max_tokens <max_tokens> --mode <mode> --reply_speed <reply_speed> --custom_prompt <custom_prompt> --test
```

- `<csv_file>`: The path to the CSV file containing the investor information
- `<temperature>`: The temperature for the GPT-3 model
- `<max_tokens>`: The maximum number of tokens for the GPT-3 model
- `<mode>`: The mode for the GPT-3 model
- `<reply_speed>`: The reply speed for the GPT-3 model
- `<custom_prompt>`: The custom prompt for the GPT-3 model
- `--test`: Run in test mode to see the generated email content without sending

## Security

Make sure to secure your sensitive information, such as your OpenAI API key and email credentials. Do not commit these to version control.
# pest-to-invest
