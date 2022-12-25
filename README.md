# Things to remember before deploying

- [ ] Verify info in [`local_settings.py`](local_settings.py) also do not forget to put the proper name of the app as the DEFAULT_FROM_EMAIL
- [ ] need to fix the domain in [`templates/my_user/password-reset-email.html`](templates/my_user/password-reset-email.html)
- [ ] send email on password being succesfully reset
- [ ] Update the welcome email
- [ ] Don't forget to actually add the search bar in lnf... coz it only works with postgresql
- [ ] Search in lnf, listings
- [ ] Uncomment search in the pages in templates folder (lnf, listings)
- [ ] add 404 and 500 pages



# Steps to Develop

## Running the Backend for ~~deployment~~ development

1. Install python 3.9 and make sure `pip` command is working fine.
2. Install `postgresql` nad `pgadmin`. Also make sure `psql` command is working fine. If you are using windows, you can use [this](https://www.postgresqltutorial.com/install-postgresql/) tutorial.
3. Create a vitual environment Run these commands:
	```bash
	pip install virtualenv
	virtualenv <name_of_virt.env>
	```

	Although you can use any name for the virtual environment. It would be better to keep the name related to the project.
4. Next activate the virtual environment:
	```bash
	source <name_of_virt.env>/bin/activate
	```
	```bash
	source <name_of_virt.env>/bin/activate
	```


## Compiling the app with backend information