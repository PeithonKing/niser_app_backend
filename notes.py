
### dynamic links
your_subdomain = "niserapp"
your_deep_link = "http://192.168.29.114:8000/lnf"  # this is the important part, the actual link
package_name = "com.example.niser_app"
fallback_link = "https://www.desmos.com/calculator"  # Do not use. Use this if you want to override the default behaviour of redirecting to playstore if app is not installed.

manual_link = f"https://{your_subdomain}.page.link/?link={your_deep_link}&apn={package_name}&afl={fallback_link}"
useful_documentation_page = "https://firebase.google.com/docs/dynamic-links/create-manually"

# Android parameters
# apn = package_name
# afl : override default behaviour of opening play store if app not installed
# amv : no need! if lower version installed, user is taken to playstore to update the app

# iOS parameters
# ibi : analogous to apn
# ifl : analogous to afl

print(manual_link)
