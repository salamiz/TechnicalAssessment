# README: Test Case for Testing SSH Connectivity using Password and Key-based Authentication

## Test Scenario

Ensure SSH connectivity and functionality using both password-based and key-based authentication methods.

## Description

This test case aims to verify the SSH connectivity to a remote server using two different authentication methods: password-based authentication and key-based authentication. The test will involve connecting to the remote server, performing a simple command to verify successful login, and disconnecting. This process will be repeated for both authentication methods.

## Setup

1. **Environment Preparation:**
    - Two machines: 
        - **Client Machine** (where the test will be initiated)
        - **Server Machine** (remote machine to connect to via SSH)
    - Ensure the SSH server (OpenSSH) is installed and running on the server machine.
    - Ensure the SSH client is installed on the client machine.

2. **Configuration for Password-based Authentication:**
    - Ensure a user account exists on the server machine.
    - Note down the username and password for the user account.

3. **Configuration for Key-based Authentication:**
    - Generate an SSH key pair on the client machine (if not already generated):
      ```sh
      ssh-keygen -t rsa -b 2048
      ```
    - Copy the public key to the server machine’s `~/.ssh/authorized_keys` file:
      ```sh
      ssh-copy-id username@server_address
      ```

## Tools Used

- SSH client (e.g., OpenSSH client)
- SSH server (e.g., OpenSSH server)
- Shell scripting for automation (optional)

## Test Steps

### Password-based Authentication

1. Open a terminal on the client machine.
2. Attempt to connect to the server using the SSH client and password:
    ```sh
    ssh username@server_address
    ```
3. When prompted, enter the password.
4. Run a simple command to verify successful login, such as `hostname` or `whoami`.
5. Check the command's output to ensure it matches the expected result (e.g., the server's hostname or the logged-in username).
6. Disconnect from the server:
    ```sh
    exit
    ```

### Key-based Authentication

1. Open a terminal on the client machine.
2. Attempt to connect to the server using the SSH client and key-based authentication:
    ```sh
    ssh username@server_address
    ```
3. Ensure no password prompt appears, indicating the key-based authentication is in use.
4. Run a simple command to verify successful login, such as `hostname` or `whoami`.
5. Check the command's output to ensure it matches the expected result (e.g., the server's hostname or the logged-in username).
6. Disconnect from the server:
    ```sh
    exit
    ```

## Teardown

1. Remove the client’s public key from the server’s `~/.ssh/authorized_keys` file (for cleanup purposes).
2. Ensure no residual connections or open sessions remain between the client and server.
3. Optionally, delete the generated SSH key pair from the client machine (if it was created specifically for this test).

## Pass/Fail Criteria

- **Pass:**
    - For password-based authentication, the client connects successfully to the server, runs the verification command, and disconnects without errors.
    - For key-based authentication, the client connects to the server without a password prompt, runs the verification command, and disconnects without errors.

- **Fail:**
    - For password-based authentication, any issues such as incorrect password prompt, inability to connect, or errors during command execution.
    - For key-based authentication, any issues such as key-based authentication failure, unexpected password prompts, inability to connect, or errors during command execution.
