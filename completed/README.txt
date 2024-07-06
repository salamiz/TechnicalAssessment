# Save the test case scenario to a .txt file

test_case_scenario = """
**Test Case: Testing SSH Connectivity Using Password and Key-based Authentication**

**Test Scenario:** Verify SSH connectivity using both password-based and key-based authentication.

#### Setup:
1. **Environment Preparation:**
    - Ensure the SSH server is installed and running on the target machine.
    - Create a user account on the target machine with a known password.
    - Generate an SSH key pair (public and private) on the client machine.
    - Copy the public key to the `~/.ssh/authorized_keys` file of the user account on the target machine.

2. **Tools Required:**
    - SSH client (e.g., `ssh` command or an SSH library like `paramiko` in Python).
    - SSH server (e.g., `sshd`).

#### Test Steps:
1. **Password-based Authentication:**
    - Execute the SSH command to connect to the target machine using the user account and password.
    - Check if the connection is established successfully.

2. **Key-based Authentication:**
    - Execute the SSH command to connect to the target machine using the user account and the private key.
    - Check if the connection is established successfully.

#### Pass/Fail Criteria:
- **Pass:** 
    - The SSH connection is established successfully using both password-based and key-based authentication.
    - The user can execute a simple command (e.g., `ls`) on the target machine without any authentication errors.
- **Fail:** 
    - The SSH connection fails using either password-based or key-based authentication.
    - Authentication errors are encountered during the connection attempt.

#### Teardown:
1. **Environment Cleanup:**
    - Remove the user account from the target machine.
    - Delete the SSH key pair from the client machine.
    - Stop the SSH server if it was specifically started for this test.

**Error Messages:**

- If the setup of the environment fails:
    - "Error: SSH server is not installed or not running on the target machine."
    - "Error: User account creation on the target machine failed."
    - "Error: SSH key pair generation on the client machine failed."
    - "Error: Copying the public key to the target machine's authorized_keys file failed."

- If password-based authentication fails:
    - "Error: SSH connection using password-based authentication failed."

- If key-based authentication fails:
    - "Error: SSH connection using key-based authentication failed."

- If any step is skipped due to the platform-specific limitations (e.g., on Windows):
    - "Info: Skipping step as it is not applicable on this platform."
"""

