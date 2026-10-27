[app]

# (str) Title of your application
title = Apple Vegas Club

# (str) Package name
package.name = applevegasclub

# (str) Package domain (needed for android packaging)
package.domain = org.applevegas

# (str) Source files where the let it be (relative to directory of spec file)
source.dir = .

# (list) Source files to include
source.exts = py,png,jpg,kv,atlas

# (list) Application version
version = 1.0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (bool) Indicate whether the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = WAKE_LOCK,INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (list) The android archs to build for
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1