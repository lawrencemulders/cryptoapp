import os
from dotenv import load_dotenv


def generate_plist_file():

    # Load environment variables from .env file
    load_dotenv()

    # Load environment variables from .env file (implementation for docker)
    env_vars = os.environ

    # Define the plist template
    plist_template = """
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.cryptoapp.docker</string>
        <key>Program</key>
        <string>/usr/local/bin/docker</string>
        <key>ProgramArguments</key>
        <array>
            <string>docker</string>
            <string>run</string>
            <string>-it</string>
            <string>--name</string>
            <string>cryptoapp</string>
            <string>--env-file</string>
            <string>app/.env</string>
            <string>cryptoapp-image</string>
        </array>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Hour</key>
            <integer>{}</integer>
            <key>Minute</key>
            <integer>{}</integer>
            <key>Weekday</key>
            <integer>{}</integer>
        </dict>
    </dict>
    </plist>
    """.format(
        env_vars.get("SCHEDULE_TIME").split(":")[0],
        env_vars.get("SCHEDULE_TIME").split(":")[1],
        env_vars.get("SCHEDULE_DAY").lower()
    )

    # Determine the appropriate directory for the plist file based on user or system-wide configuration
    launchd_dir = os.path.expanduser("~/Library/LaunchAgents/")

    # Create directory if it doesn't exist
    os.makedirs(launchd_dir, exist_ok=True)

    # Define the path to the plist file
    plist_path = os.path.join(launchd_dir, "launchd_job.plist")

    # Write the plist content to a file
    with open(plist_path, "w") as plist_file:
        plist_file.write(plist_template)
        print(f"Generated plist file: {plist_path}")
        print(f"With the following plist file: {plist_template}")
