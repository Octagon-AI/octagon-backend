import os
from lighthouseweb3 import Lighthouse
from dotenv import load_dotenv

class LighthouseClient:
    def __init__(self, api_key_env_var='LIGHTHOUSE_API_KEY'):
        load_dotenv()
        self.api_token = os.getenv(api_key_env_var)

        if self.api_token is None:
            raise EnvironmentError(f"API token not found. Please set {api_key_env_var} in your environment.")

        self.client = Lighthouse(token=self.api_token)


class FilecoinRetriever(LighthouseClient):
    def __init__(self, api_key_env_var='LIGHTHOUSE_API_KEY'):
        super().__init__(api_key_env_var)

    def download_file(self, file_cid, destination_path):
        try:
            file_info = self.client.download(file_cid)  # The file_info is a tuple containing the file content and its metadata

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


class FilecoinUploader(LighthouseClient):
    def __init__(self, api_key_env_var='LIGHTHOUSE_API_KEY'):
        super().__init__(api_key_env_var)

    def upload_file(self, source_file_path, tag=None):
        try:
            if tag:
                upload = self.client.upload(source=source_file_path, tag=tag)
                print("File Upload with Tag Successful!")
            else:
                upload = self.client.upload(source=source_file_path)
                print("Regular File Upload Successful!")
            return upload

        except Exception as e:
            print("An error occurred during the upload:", str(e))


# Example usage:
if __name__ == "__main__":
    # Example download usage
    retriever = FilecoinRetriever()
    file_cid = "bafkreieqpy57ec3x3k6iospywfjakiddb5vjgkzovwitvb5zs7au5hwsyq"
    destination_path = "./downloaded_file.txt"
    retriever.download_file(file_cid, destination_path)

    # Example upload usage
    uploader = FilecoinUploader()
    source_file_path = "./requirements.txt"
    uploader.upload_file(source_file_path, tag="example_tag")
