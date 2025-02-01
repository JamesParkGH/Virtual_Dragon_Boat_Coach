import subprocess
import sys

def main(session_url, token, trial_name):
    # Run BatchDownload.py
    try:
        subprocess.run([
            'python', 'batchDownload.py',
            session_url,
            token  # Pass token to the script
        ], check=True)

        # Run runOpensim.py
        session_id = session_url.split('/')[-1]
        subprocess.run([
            'python', 'runOpensim.py',
            session_id,  # Pass session ID
            trial_name   # Pass trial name
        ], check=True)

        print("Files downloaded and processed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during process: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <session_url> <token> <trial_name>")
        sys.exit(1)

    session_url = sys.argv[1]
    token = sys.argv[2]
    trial_name = sys.argv[3]

    main(session_url, token, trial_name)
