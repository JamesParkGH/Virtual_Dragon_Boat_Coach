from utilsOpensim import download_session
import os
import sys

# Get the session URL passed from the web form
sessionURL = sys.argv[1].strip()

# Extract the session ID from the URL
session_id = sessionURL.split('/')[-1]

# Base directory for downloads
downloadPath = os.path.join(os.getcwd(), 'Data')

# Download data for the specified session
download_session(session_id, sessionBasePath=downloadPath, downloadVideos=True)
