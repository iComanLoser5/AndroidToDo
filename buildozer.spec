[app]

# (str) Title of your application
title = ToDo List

# (str) Package name (must be lowercase, no spaces)
package.name = todolist

# (str) Package domain (reverse domain notation is typical)
package.domain = com.gurtaj

# (str) Source code directory (where main.py lives)
source.dir = .

# (list) Source files to include (leave empty to include everything)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 0.1

# (list) Application requirements
# Add all libraries your app needs (example includes kivy and kivymd).
requirements = python3,kivy,kivymd

# (list) Supported orientations: 'landscape', 'portrait', etc.
orientation = portrait

# (bool) Fullscreen mode (1 = fullscreen, 0 = not fullscreen)
fullscreen = 0

# (list) Permissions needed by your app
# Uncomment or add others if you read/write files or use the internet
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enables Android auto backup feature
android.allow_backup = True

# (str) Format to package the app for debug (apk or aar)
android.debug_artifact = apk

# (str) Format to package the app for release (aab, apk, or aar)
# Uncomment the line below and set to 'aab' if publishing on Google Play
# android.release_artifact = aab


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if running as root (0 = False, 1 = True)
warn_on_root = 1
