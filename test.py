import os
from dotenv import load_dotenv
load_dotenv()
lst = os.getenv('lst')
print(lst.split()[0])