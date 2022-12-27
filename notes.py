
### dynamic links
your_subdomain = "127.0.0.1:8000"
your_deep_link = ""  # this is the important part, the actual link
package_name = "com.example.niser_app"
minimum_version = "19"
fallback_link = ""  # Do not use. Use this if you want to override the default behaviour of redirecting to playstore if app is not installed.

manual_link = f"https://{your_subdomain}.page.link/?link={your_deep_link}&apn={package_name}[&amv={minimum_version}][&afl={fallback_link}]"
useful_documentation_page = "https://firebase.google.com/docs/dynamic-links/create-manually"

# Android parameters
# apn = package_name
# afl : override default behaviour of opening play store if app not installed
# amv : no need! if lower version installed, user is taken to playstore to update the app

# iOS parameters
# ibi : analogous to apn
# ifl : analogous to afl





