import os
import sys

# Inject token before importing utilsOpensim
token = sys.argv[2].strip()  # Get token from command-line arguments
os.environ["API_TOKEN"] = token  # Set token in environment

from utilsOpensim import download_session  # Import AFTER setting API_TOKEN

sessionURL = sys.argv[1].strip()
session_id = sessionURL.split('/')[-1]
downloadPath = os.path.join(os.getcwd(), 'Data')

# Now download_session() will use the token from environment
download_session(session_id, sessionBasePath=downloadPath, downloadVideos=True)