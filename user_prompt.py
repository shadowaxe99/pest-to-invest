class UserPrompt:
    @staticmethod
    def get_signature():
        with open('email_signature.txt', 'r') as f:
            signature = f.read()
        return signature
