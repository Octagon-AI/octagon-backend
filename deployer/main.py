import os
from dotenv import load_dotenv

ETHERSCAN_API_KEY = 'N8SP1UH648EFP6486Y2KZA8DYQPU3Y7RRM'
PRIVATE_KEY = '0x6ce33f56575ff4bad9cd94f1d9bd22bb54eb4061a54bf0889a7af1e6f65619a1'
RPC_URL = 'https://sepolia.rpc.thirdweb.com/'

# Load environment variables from .env file
load_dotenv()

contract_path = os.path.join(os.getcwd(), "Verifier.sol")
print(contract_path)
with open(contract_path, "r", encoding="utf8") as source_file:
    source = source_file.read()

    # print(source)


import subprocess
import re

# Running a simple command
# result = subprocess.run(["ls"], capture_output=True, text=True)


def copy_files(to_dir):
    try:
        _result = subprocess.run(
            ["cp", "Verifier.sol", f"{to_dir}/src"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("File copied successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        print(f"Error message: {e.stderr}")



def deploy_contract(to_dir):
    try:

        command = f"cd {to_dir} && forge create --rpc-url {RPC_URL} --private-key {PRIVATE_KEY} src/Verifier.sol:Halo2Verifier"
        

        # Run the command
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
    
        match = re.search(r"Deployed to: (0x[a-fA-F0-9]{40})", result.stdout)
        if match:
            deployed_address = match.group(1)
            print(f"Deployed Contract Address: {deployed_address}")
            
            return deployed_address
        else:
            print("Deployed contract address not found in the output.")
        
    except subprocess.CalledProcessError as e:
        # Print the error message and return code
        print(f"Command failed with return code {e.returncode}")
        print(f"Error message: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


def verify_contract(to_dir, contract_address):
    try:
        command = f"cd {to_dir} && forge verify-contract --chain-id 11155111 --watch --etherscan-api-key {ETHERSCAN_API_KEY} {contract_address} src/Verifier.sol:Halo2Verifier"
        
        # Run the command
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
    
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # Print the error message and return code
        print(f"Command failed with return code {e.returncode}")
        print(f"Error message: {e.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")


def deploy_main():
    to_dir = "deployer-env"
    
    copy_files(to_dir)
    deployed_address =  deploy_contract(to_dir)
    verify_contract(to_dir, deployed_address)


if __name__ == "__main__":
    deploy_main()
