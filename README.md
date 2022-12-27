<!-- Ignore #MD031 #MD010 -->

# Things to Remember Before Deploying

- [ ] Verify info in [`local_settings.py`](local_settings.py) also do not forget to put the proper name of the app as the DEFAULT_FROM_EMAIL
- [ ] need to fix the domain in [`templates/my_user/password-reset-email.html`](templates/my_user/password-reset-email.html)
- [ ] send email on password being succesfully reset
- [ ] Update the welcome email
- [ ] Don't forget to actually add the search bar in lnf... coz it only works with postgresql
- [ ] Search in lnf, listings
- [ ] Uncomment search in the pages in templates folder (lnf, listings)
- [ ] add 404 and 500 pages

# Steps to Develop

## Setting up Firebase

Hope you have flutter installed and flutter doctor says all fine. If not, you can follow [this](https://flutter.dev/docs/get-started/install) tutorial.

1. Go to [Firebase Console](https://console.firebase.google.com/) and create a new project. No need to add google analytics or anything else. Just create a new project by accepting the terms and conditions.
2. Install the firebase cli following [this](https://firebase.google.com/docs/cli#install_the_firebase_cli) tutorial.
3. From any directory, run this command:
	```bash
	dart pub global activate flutterfire_cli
	```
	you can get these steps by following the following steps:
	**Go to your app, -> settings button beside Project Overview, -> project settings, -> general -> Under `your apps`, you have to make a new app for flutter (click on the flutter icon)**, and follow the steps along.
	Then, at the root of your Flutter project directory, run this command:
	```bash
	flutterfire configure --project=<project_ name>
	```

4. If you have followed the steps, as you will click on `continue to console`, you will see that an app has been created. For your informaton, the app was not created by you clicking on the website, the app was created by running the commands mention above. Now you need to add the firebase configuration to the app. For that, you need to download the `google-services.json` file from the firebase console. You can find that in the app you you have created. Finally move the file to the `android/app` directory of your Flutter project.
5. Next you have to download the key file for the service account from the firebase console. You can find that in the
	**project settings -> Service Accounts -> Firebase Admin SDK -> Python -> Generate new Private key**.
6. **Now you should complete the [next part (setup django backend)](#setup-django-project). After completing that return here to complete this step.**
	- Move the key file to the root directory of the Django project.
	- make a new environment variable named `GOOGLE_APPLICATION_CREDENTIALS` and set it to the path+name of the key file. Now as this file has already been kept in the root directory of your django project, the path will be something like this:
	```bash
	<path_to_project>/niser_app_backend/<name_of_key_file>.json
	```
	(**To make a new environment variable in Windows** you can search *env* in the start menu and click on *Edit the system environment variables* and then click on *Environment Variables...* button at the bottom under the advanced tab. Then click on *New...* button in the *User variables* section. In the *Variable name* field type `GOOGLE_APPLICATION_CREDENTIALS` and for the *Variable value* field type click on the *Browse File...* option. Then navigate to the key file and select it. Then click on *OK* button. Now you have created a new environment variable. Once you have completed this step, you can **restart** your system.)

## Setup Django Project

1. Install python 3.9 and make sure `pip` command is working fine. Other Python versions might work, but I have not tested them. ~~Please don't even think about Anaconda Distribution. I would recommend to uninstall Anaconda Distribution or any other python version if you have it installed already. Crossing this because this is informal discussion... like Snape's copy of `Advanced Potion-Making`.~~
2. Install `postgresql` and optionally `pgadmin`. Also make sure `psql` command is working fine.
3. Make a database in postgreql with a name of your choice. You can use pgadmin for this, or you can use the following command in psql shell (asuming you want to login using the default user `postgres`):
	```bash
	psql -U postgres -h 127.0.0.1  # this will open the psql shell
	```
	Now to create the database use the following command in the psql shell (Remember to replace `<name_of_db>` with the name of your choice. Remember this name as you will need it later):
	```psql
	create database <name_of_db>
	```
	You can also create a new user for the database and give the database access to it. If you opt for that, I hope you know how to do that, and what changes you will have to make later. However in future steps I will assume that you are using the default user `postgres` for the database.
4. clone the repository by running the following command:
	```bash
	git clone https://github.com/PeithonKing/niser_app_backend.git
	```
5. Create a vitual environment Run these commands:
	```bash
	pip install virtualenv  # installing virtualenv python package
	virtualenv <name_of_virt.env>  # creating virtual environment
	```

	Although you can use any name for the virtual environment. It would be better to keep the name related to the project.
6. Next activate the virtual environment by either of the following commands depending on your OS:
	```bash
	source <name_of_virt.env>/bin/activate  # for linux/mac
	./<name_of_virt.env>/Scripts/activate  # for windows
	```
7. Now move into the folder and install the requirements by running the following command:
	```bash
	pip install -r requirements.txt
	```

After completing upto this step, you can go back to the [previous part (setting up firebase)](#setting-up-firebase) to complete the step 6.

## Settings for django project

1. Make a copy of the  [`niser_app\local_settings_example.py`](niser_app\local_settings_example.py) file and rename the copy as `local_settings.py`. Now keep the example file as it is and change the [`niser_app\local_settings.py`](niser_app\local_settings.py) file folowing the next steps.
2. Connect to the internet, open a terminal and type `ipconfig` (`ifconfig` for linux/mac) and note down the **IPv4** address. This is your local IP address. Now, in the `local_settings.py` file write your local IP address beside `IP`. As for the port number, you can keep this to be 8000. If it is already in use, you can change it to any other free port number.
3. In line 11, add your email address. As this is supposed to be a development server, you can use your personal email address. This is the email address people will recieve emails from when they register or reset their password. You cannot use a fake/dummy email address for this.
4. Now go to the Security tab of your google account and make sure 2 step verification is enabled. Then go to the App passwords tab and generate a new app password for the app `niser_app` and note it down. Now in line 12, add the password you have just noted down.
5. In line 15, add the Name of the App. This is the name that will be displayed in the email. While I am writing this README file, the name of the app wasn't fixed yet. So I have kept it as `SDG App`. You can change it to whatever you want.
6. In line 17, add the name of the key file for the service account you have downloaded in step 5 of the [setting up firebase](#setting-up-firebase). You don't need to add the path, just the name of the file will suffice.
7. In line 24, 33, 34 and 35 make the required changes.
8. Finally open a terminal, navigate to the root directory of the project and run the following command:
	```bash
	python manage.py migrate
	python manage.py makemigrations
	```
	This will create the required tables in the database.
9. Now make a superuser by running the following command:
	```bash
	python manage.py createsuperuser
	```
	You will be asked to enter a username, email and password. You can enter anything you want. But remember the username and password as you will need them later.
10. Now run the following command to start the server:
	```bash
	python manage.py runserver <your_local_ip>:<port_number>  # same as you have put in the local_settings.py file
	```
11. Open a browser and see if the server is running by going to the following url:
	```url
	http://<your_local_ip>:<port_number>/admin
	```
	If you see the admin page, then you have successfully setup the django project. If you don't see the admin page, then you have done something wrong. Please check the steps again and try to fix the error. If you are still unable to fix the error, then please open an issue in the github repository.

	You will be able to login to the admin page using the username and password you have created in step 9.
