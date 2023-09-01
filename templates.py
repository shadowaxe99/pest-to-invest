class Templates:

    def __init__(self) -> None:
        
        self.template = """Hi [NAME], I hope this email finds you well. I wanted to reach out to introduce myself and express my interest in your company, [COMPANY NAME]. I have been following your work and I am impressed with the innovative solutions you provide.

        I would love to learn more about your company and explore potential collaboration opportunities. Please let me know if you would be available for a call or meeting to discuss further.

        Thank you for your time and consideration. I look forward to hearing from you.

        Best regards,
        [Your Name]"""

    def get_template(self):
        return self.template
    def format_email_body(self, raw_body):
        return raw_body
    def format_follow_up_subject(self, raw_subject):
        return raw_subject
    
    @staticmethod
    def sign():
        with open('email_signature.txt', 'r') as f:
            signature = f.read()
            return signature
