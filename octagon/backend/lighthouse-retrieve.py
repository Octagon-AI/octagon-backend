import io
import os
from lighthouseweb3 import Lighthouse
# os.environ['LIGHTHOUSE_API_KEY'] = 'f9aa7723.749dd94a4bad4392a947dc5aed3c24db'
from dotenv import load_dotenv

load_dotenv()

# Get the API token from the environment variable
api_token = os.getenv('LIGHTHOUSE_API_KEY')

if api_token is None:
    raise EnvironmentError("API token not found. Please set LIGHTHOUSE_API_KEY in your environment.")

# Initialize Lighthouse client
lh = Lighthouse(token=api_token)

# Replace "YOUR_CID_TO_DOWNLOAD" with the actual CID of the file you want to download
file_cid = "bafkreieqpy57ec3x3k6iospywfjakiddb5vjgkzovwitvb5zs7au5hwsyq"
destination_path = "./downloaded_file.txt"

try:
    file_info = lh.download(file_cid)  # The file_info is a tuple containing the file content and its metadata

    if file_info and len(file_info) > 0:
        file_content = file_info[0]  # Extract file content
        headers = file_info[1]  # Extract headers

        # Debug information
        print("Response headers:", headers)

        # Handle missing content-length header gracefully
        if 'content-length' in headers:
            content_length = headers['content-length']
            print(f"Content-Length: {content_length}")
        else:
            print("Warning: 'content-length' header is missing.")

        # Save the downloaded file to the destination path
        with open(destination_path, 'wb') as destination_file:
            destination_file.write(file_content)

        print("Download successful! File saved to:", destination_path)
    else:
        print("Error: No file content received.")

except Exception as e:
    print("An error occurred during the download:", str(e))
