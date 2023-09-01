from templates import Templates
class UserPrompt:
    @staticmethod
    def get_signature():
        with open('email_signature.txt', 'r') as f:
            signature = f.read()
            return signature
    def get_prompt(self):
        templates = Templates()
        return templates.get_template()
