# NeXess - Backend

The backend for my final year project during BSc Computer Science at Queen Mary University of London. An NFC based access control application.

## Project Hardware Requirements

The project requires the following hardware:

- an NFC capable Android phone running **Android 7.0 (Nougat, API 24)** or higher, with an NFC tag utility application installed (developed using the [NFC Tools app](https://play.google.com/store/apps/details?id=com.wakdev.wdnfc&hl=en_GB))
- a laptop/computer with Android Studio installed
- writeable NFC tag(s) (developed using Mifare Classic NfcA tags)

> ## Disclaimer
>
> **This project works on your local network, using your laptop's current IP address as a server URL. It needs both the phone and machine running the server to be connected to the same WiFi network**
>
> **Also take note that eduroam and similar WiFi networks will not allow the traffic the project generates. If these kinds of networks are the only available network around, use the mobile network hotspot of a different mobile phone instead.**

## Setup instructions

To run & test this project on your own machine, follow the steps below. After setting up the backend, you will need to follow [the frontend application's](https://github.com/kdVincler/NeXess-frontend) setup instructions to be able to fully run the project.

1. After cloning/downloading this repository, create a [conda](https://docs.anaconda.com/miniconda/install/) environment for this project and activate the environment:

   ```console
   (base)$ conda create --name nexess python=3.11
   (base)$ conda activate nexess
   ```

2. Navigate to the cloned/downloaded repository directory and with the conda environment active, install the backend (Python) dependencies:

   ```console
   (nexess)$ pip install -r requirements.txt
   ```

3. Create a development database: (should return "No migrations to apply." and a `db.sqlite3` file should be created)

   ```console
   (nexess)$ python manage.py migrate
   ```

4. Create a superuser (admin user). Run the following command and follow the instructions (fill in username, email, password and confirm password). This account will be used to create other users, register doors and update permissions.

   ```console
   (nexess)$ python manage.py createsuperuser
   ```

5. In the root directory of your cloned/downloaded version of the repository (i.e. the same folder this README file is in) create a file called `.env` and in it declare & set a variable called `IP_ADDRESS` to your laptop's current IP address as shown below (can be achieved with opening the created `.env` file in any text editor)

   ```python
   IP_ADDRESS="YOUR_IP_ADDRESS_HERE"
   ```

6. If everything goes smoothly, you should be able to start the Django development server from the root directory and broadcast it on the local network:

   ```console
   $ python manage.py runserver 0.0.0.0:8000
   ```

Your server now should be reachable on 3 different URLs.

- http://localhost:8000/
- http://127.0.0.1:8000/
- http://`IP_ADDRESS`:8000/ (where `IP_ADDRESS` is declared in `.env` - **only reachable for other devices on the network**)

If you would like to test if the server is running correctly, go to either of the following URLs and you should see a "Server reached (200 - OK)" message in your browser:

- http://localhost:8000/health/
- http://127.0.0.1:8000/health/

The admin page, where the created superuser can manipulate the data of the project is accessible on the following URLs:

- http://localhost:8000/admin/
- http://127.0.0.1:8000/admin/

You can use the standard keyboard interrupt (Ctrl + C) to stop the server at any time. Closing the terminal window where runserver was called will also stop the server. The '0.0.0.0:8000' command is needed to make the server reachable on the local network.

### A note on the `IP_ADDRESS` environmental variable.

Every time your IP address changes (i.e. you try to run the project on a different network then when local setup happened), you need to edit the value of `IP_ADDRESS` in `.env`, save the file, (if the development server was running, stop the server) and start the development server with the command shown in step 6 of the setup instructions.

## Usage

- **Create a regular user:** Log in to the admin site with your superuser and click on "+ Add" next to Users. Fill in username, password, confirm password, first name, last name and press save. Apart from a new user being created, a new Permission entry will be created as well with a default permission level of Level 0 - Guest.

- **Change user permission level:** Navigate to the Permissions table and select the name of the user thar you would like to edit the permission level for. Use the dropdown to select the desired permission level and click save.

- **Door registration:** Click on "+ Add" next to Doors. Fill in the description field and select desired permission level needed to open the door using the dropdown and then click save.

- **How door opening and permissions work:** Every user that has a permission level higher or equal to the permission level of the door can enter. Any user with a lower permission level than the door is unable to proceed and is returned an error saying just that. Both successful and unsuccessful door openings result in a Log entry being made with a reference to the user, the door, the date time of the log entry and a Boolean flag indicating the opening attempt's result.

- **Searching, filtering, ordering:** An admin (Staff + Superuser) account can search, filter and change the displayed order of every table in the server's database (Users, Doors, Logs and Permissions). Filtering is controlled by the tile right to the table rows, searching by the search bar above them and ordering by the clickable column names.

- **Relationship of tables:** Deleting or editing any table entry will delete or change the entries dependant on said entry accordingly (i.e. deleting a user will delete the related log entries and permission entry; Deleting a door will delete the related log entries; editing a user's username/first name/last name will be observable in any related log or permission entries; etc. )
