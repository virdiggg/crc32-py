class StrHelper:
    def prGreen(self, skk):
        print("\033[92m {}\033[00m" .format(skk))

    def prRed(self, skk):
        print("\033[91m {}\033[00m" .format(skk))

    def clean_utf8(self, text):
        # Encode to bytes, ignoring errors, then decode back to string
        return text.encode('utf-8', 'ignore').decode('utf-8')
