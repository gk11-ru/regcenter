import base64, sys

print base64.urlsafe_b64decode(sys.argv[1].strip(':'))