from dotenv import dotenv_values
import os


def generate_plist_file():

    # Load environment variables from .env file
    env_vars = dotenv_values(".env")

    # Define the plist template
    plist_template = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.cryptoapp.docker</string>
        <key>Program</key>
        <string>/cryptoapp/docker/Dockerfile</string>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Hour</key>
            <integer>{env_vars["SCHEDULE_TIME"].split(":")[0]}</integer>
            <key>Minute</key>
            <integer>{env_vars["SCHEDULE_TIME"].split(":")[1]}</integer>
            <key>Weekday</key>
            <integer>{env_vars["SCHEDULE_DAY"].lower()}</integer>
        </dict>
    </dict>
    </plist>
    """

    # Determine the appropriate directory for the plist file based on user or system-wide configuration
    launchd_dir = os.path.expanduser("~/Library/LaunchAgents/")

    # Define the path to the plist file
    plist_path = os.path.join(launchd_dir, "my_launchd_job.plist")

    # Remove the existing plist file if it exists, allow for new config settings
    if os.path.exists(plist_path):
        os.remove(plist_path)

    # Write the plist content to a file
    plist_path = os.path.join(launchd_dir, "launchd_job.plist")
    with open(plist_path, "w") as plist_file:
        plist_file.write(plist_template)

    print(f"Generated plist file: {plist_path}")
