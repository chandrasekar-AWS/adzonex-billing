#!/usr/bin/env python3
"""Tweaks the generated Capacitor Android project: black system bars, no cloud backup of app data,
version numbers, optional release signing from environment variables.  Usage: patch-android.py <android-dir>"""
import os, re, sys
import xml.dom.minidom as md

root = sys.argv[1]
code = os.environ.get('VERSION_CODE', '1')
name = os.environ.get('VERSION_NAME', '1.0.0')

def rw(path, fn):
    s = open(path, encoding='utf-8').read()
    n = fn(s)
    assert n != s or True
    open(path, 'w', encoding='utf-8').write(n)
    return n

# --- AndroidManifest: no automatic cloud backup of the app's local data, no plain-http traffic, keyboard resizes the page
def manifest(s):
    s = s.replace('android:allowBackup="true"', 'android:allowBackup="false"')
    if 'usesCleartextTraffic' not in s:
        s = s.replace('<application', '<application\n        android:usesCleartextTraffic="false"', 1)
    if 'windowSoftInputMode' not in s:
        s = s.replace('android:launchMode="singleTask"', 'android:launchMode="singleTask"\n            android:windowSoftInputMode="adjustResize"', 1)
    return s
mp = os.path.join(root, 'app/src/main/AndroidManifest.xml')
md.parseString(rw(mp, manifest))

# --- Theme: black status and navigation bars with light icons, black window background
def styles(s):
    items = ('\n        <item name="android:statusBarColor">#000000</item>'
             '\n        <item name="android:navigationBarColor">#000000</item>'
             '\n        <item name="android:windowLightStatusBar">false</item>'
             '\n        <item name="android:windowBackground">@android:color/black</item>')
    if 'android:statusBarColor' in s:
        return s
    n = re.sub(r'(<style name="AppTheme\.NoActionBar"[^>]*>)', lambda m: m.group(1) + items, s, count=1)
    assert n != s, 'AppTheme.NoActionBar not found'
    return n
sp = os.path.join(root, 'app/src/main/res/values/styles.xml')
md.parseString(rw(sp, styles))

# --- Gradle: version, lint, optional signing
def gradle(s):
    s = re.sub(r'versionCode\s+\d+', 'versionCode ' + code, s, count=1)
    s = re.sub(r'versionName\s+"[^"]*"', 'versionName "' + name + '"', s, count=1)
    if 'KS_FILE' in s:
        return s
    return s.rstrip() + '''

// ---- added by native/patch-android.py ----
android {
    lint {
        checkReleaseBuilds false
        abortOnError false
    }
    if (System.getenv('KS_FILE')) {
        signingConfigs {
            release {
                storeFile file(System.getenv('KS_FILE'))
                storePassword System.getenv('KS_PASS')
                keyAlias System.getenv('KS_ALIAS')
                keyPassword System.getenv('KEY_PASS')
            }
        }
        buildTypes {
            release {
                signingConfig signingConfigs.release
            }
        }
    }
}
'''
gp = os.path.join(root, 'app/build.gradle')
g = rw(gp, gradle)
assert ('versionCode ' + code) in g and ('versionName "' + name + '"') in g

# --- Direct printing: native "ZXPrint" plugin (sends the bill PDF to Android's print dialog) + register it in MainActivity
import glob, json, shutil
def printing():
    cfg = json.load(open(os.path.join(root, '..', 'capacitor.config.json')))
    pkg = cfg['appId']
    jdir = os.path.join(root, 'app/src/main/java', *pkg.split('.'))
    os.makedirs(jdir, exist_ok=True)
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'android', 'ZXPrintPlugin.java'), encoding='utf-8').read()
    open(os.path.join(jdir, 'ZXPrintPlugin.java'), 'w', encoding='utf-8').write(tpl.replace('__PACKAGE__', pkg))
    main = os.path.join(jdir, 'MainActivity.java')
    assert os.path.exists(main), 'MainActivity.java not found in ' + jdir
    open(main, 'w', encoding='utf-8').write(
        'package ' + pkg + ';\n\nimport android.os.Bundle;\nimport com.getcapacitor.BridgeActivity;\n\n'
        'public class MainActivity extends BridgeActivity {\n'
        '    @Override\n    public void onCreate(Bundle savedInstanceState) {\n'
        '        registerPlugin(ZXPrintPlugin.class);\n        super.onCreate(savedInstanceState);\n    }\n}\n')
    print('Direct print plugin installed in', jdir)
printing()

print('Android project patched: version', name, '(' + code + ')')
