import instaloader
from instaloader.exceptions import ConnectionException, ProfileNotExistsException, QueryReturnedNotFoundException
from datetime import datetime
import pytz
import json
from dotenv import load_dotenv #import and load .env
import getpass  # For securely entering passwords
import os   # For directory handling
import sys  # For exiting the program
import time # For timesleep
import random # For random timesleep

load_dotenv()

def convert_utc_to_timezone(dt, timezone_str):
    # Create timezone object from string
    timezone = pytz.timezone(timezone_str)
    # Convert datetime to the specified timezone
    return dt.astimezone(timezone)

def scrape_instagram_profile(username, year, month):
    # Create an instance of Instaloader
    L = instaloader.Instaloader()

    #proxie settings
    proxies = {
        "socks5": os.getenv("socks5") #socks5 Proxy
    }
    L.context._session.proxies = proxies

    try:
        # Log in the user
        L.login(USERNAME, PASSWORD)
        print("Logged in successfully!")
    except instaloader.exceptions.ConnectionException:
        print("Failed to connect to Instagram. Check your connection.")
    except instaloader.exceptions.BadCredentialsException:
        print("Invalid credentials. Check your username or password.")

    try:
        # Load the profile
        profile = instaloader.Profile.from_username(L.context, username)
    except ProfileNotExistsException:
        print(f"Profile {username} does not exist.")
        sys.exit()  # Exit the application
    except ConnectionException:
        print("Failed to connect to Instagram. Check your connection.")
        sys.exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()

    # Print profile details
    print(f"Profile: {profile.username}")
    print(f"Followers: {profile.followers}")
    print(f"Following: {profile.followees}")
    print(f"Posts: {profile.mediacount}")

    # Define timezone-aware dates in UTC
    timezone_utc = pytz.UTC
    
    # Handle month transition for December
    start_date_utc = datetime(year, month, 1, tzinfo=timezone_utc)
    if month == 12:
        end_date_utc = datetime(year + 1, 1, 1, tzinfo=timezone_utc)
    else:
        end_date_utc = datetime(year, month + 1, 1, tzinfo=timezone_utc)

    # Convert start_date and end_date to the target timezone
    start_date = convert_utc_to_timezone(start_date_utc, 'Asia/Jakarta')
    end_date = convert_utc_to_timezone(end_date_utc, 'Asia/Jakarta')

    # Track if posts were found in the given date range
    posts_found = False

    # Create a list to store post data
    post_data_list = []

    # Download, Collect and save data
    for post in profile.get_posts():
        post_date = post.date_local.replace(tzinfo=pytz.UTC)  # Ensure post date is timezone-aware
        post_date_local = convert_utc_to_timezone(post_date, 'Asia/Jakarta')
        if start_date <= post_date_local < end_date:
            posts_found = True  # A post was found in the date range
            print(f"Collecting post {post.shortcode}")
            try:
                # Download the post
                # L.download_post(post, target=f"{profile.username}_posts_{year}_{month}")

                # Collect post data
                if post.is_video:
                    post_type = "video"
                else:
                    post_type = "photo"
                post_data = {
                    "shortcode": post.shortcode,
                    "date": post_date_local.strftime("%Y-%m-%d %H:%M:%S"),
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "post_type": post_type,
                }
                post_data_list.append(post_data)
                time.sleep(random.randint(12, 15))

            except QueryReturnedNotFoundException:
                print(f"Post {post.shortcode} could not be downloaded.")
            except Exception as e:
                print(f"An error occurred while downloading post {post.shortcode}: {e}")

    # Check if no posts were found
    if not posts_found:
        print(f"No posts found for {username} in {year}-{month}. Exiting application.")
    else:
        print("All posts have been downloaded.")


        # Define the directory to save the JSON file
        output_dir = f"json/{username}"        
        # Check if the directory exists, if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' created.")
        else:
            print(f"Directory '{output_dir}' already exists.")
        # Save the collected post data to a JSON file
        json_filename = os.path.join(output_dir, f"{username}_posts.json")
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(post_data_list, json_file, ensure_ascii=False, indent=4)
        
        print(f"Post data has been saved to {json_filename}.")

    sys.exit()  # Exit the application after the process is complete

if __name__ == "__main__":
    # Prompt user for their Instagram login details
    USERNAME = input("Enter your Instagram username: ")
    PASSWORD = getpass.getpass("Enter your Instagram password: ")
    # Prompt Instagram Target
    username = input("Enter the Instagram username to scrape: ")
    try:
        year = int(input("Enter the year (e.g., 2024): "))
        month = int(input("Enter the month (1-12): "))
        if month < 1 or month > 12:
            print("Month should be between 1 and 12.")
            sys.exit()  # Exit if the month input is invalid
        else:
            scrape_instagram_profile(username, year, month)
    except ValueError:
        print("Invalid input for year or month. Please enter valid numbers.")
        sys.exit()  # Exit if the input is invalid
