import asyncio       # Handles asynchronous event loop (core engine of the server)
import asyncssh      # Library that implements SSH protocol in Python
import sys           # Used to get the current Python interpreter path
import os            # File paths and environment variables



# SSH SERVER DEFINITION

class PortfolioSHHServer(asyncssh.SSHServer):

    # Disable authentication → allows anyone to connect (for demo purposes)
    def begin_auth(self, username):
        return False

    # Required to allow a session to start (fixes random connection drops)
    def session_requested(self):
        return True

    # Runs when a client connects
    def connection_made(self, conn):
        print(f'Connection from {conn.get_extra_info("peername")[0]}')

    # Runs when a client disconnects or an error occurs
    def connection_lost(self, exc):
        if exc:
            print(f'Connection error: {exc}')



# CLIENT HANDLER (CORE LOGIC)

async def handle_client(process):

    # Path to your portfolio script (same folder as this file)
    script_path = os.path.join(os.path.dirname(__file__), 'portfolio.py')

    # Path to the current Python interpreter
    python_path = sys.executable

    # Create a MUTABLE copy of environment variables
    # (fixes "mappingproxy" error)
    env = dict(os.environ)

    # Ensure terminal supports colors and proper formatting
    env['TERM'] = 'xterm-256color'
    

    # Start your portfolio script as a subprocess
    proc = await asyncio.create_subprocess_exec(
        python_path, script_path,

        # Connect SSH input/output directly to your script
        stdin=process.stdin,
        stdout=process.stdout,
        stderr=process.stderr,

        # Pass modified environment
        env=env
    )

    # Wait until the portfolio script finishes running
    await proc.wait()

    # Close SSH session cleanly
    process.exit(0)



# START SSH SERVER

async def start_server():
    await asyncssh.create_server(

        # Use our custom SSH server class
        PortfolioSHHServer,

        # Listen on all network interfaces (0.0.0.0)
        '',
        
        # Port number (use 2222 locally, later switch to 22 in production)
        2222,

        # SSH host key (server identity)
        server_host_keys=['ssh_host_key'],

        # Function that handles each connection
        process_factory=handle_client,
    )



# MAIN ENTRY POINT

async def main():

    print("Generating host key...")

    # Generate SSH key if it doesn't exist
    if not os.path.exists('ssh_host_key'):
        keygen = await asyncio.create_subprocess_exec(
            'ssh-keygen',
            '-t', 'ed25519',      # Key type (modern + secure)
            '-f', 'ssh_host_key', # Output file
            '-N', ''              # No passphrase
        )
        await keygen.wait()

    print("Starting SSH server on port 2222...")

    # Start the SSH server
    await start_server()

    print("Server running. Connect with: ssh -p 2222 localhost")

    # Keep the server running forever
    await asyncio.Future()



# RUN PROGRAM

if __name__ == '__main__':
    asyncio.run(main())