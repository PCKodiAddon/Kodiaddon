import os
import xml.etree.ElementTree as ET
import hashlib
import zipfile
from datetime import datetime
import shutil

def generate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def create_addon_xml():
    addon = ET.Element("addon")
    addon.set("id", "plugin.video.weebaymodz")
    addon.set("name", "WeebayModz")
    addon.set("version", "1.0.0")
    
    requires = ET.SubElement(addon, "requires")
    import_xbmc = ET.SubElement(requires, "import")
    import_xbmc.set("addon", "xbmc.python")
    import_xbmc.set("version", "3.0.0")
    
    extension = ET.SubElement(addon, "extension")
    extension.set("point", "xbmc.python.pluginsource")
    extension.set("library", "addon.py")
    
    extension_provides = ET.SubElement(extension, "provides")
    extension_provides.text = "video"

    extension_metadata = ET.SubElement(addon, "extension")
    extension_metadata.set("point", "xbmc.addon.metadata")
    
    summary = ET.SubElement(extension_metadata, "summary")
    summary.text = "WeebayModz Addon"
    
    description = ET.SubElement(extension_metadata, "description")
    description.text = "WeebayModz Kodi Video Addon"
    
    platform = ET.SubElement(extension_metadata, "platform")
    platform.text = "all"
    
    return ET.ElementTree(addon)

def create_repository_addon_xml():
    addon = ET.Element("addon")
    addon.set("id", "repository.weebaymodz")
    addon.set("name", "WeebayModz Repository")
    addon.set("version", "1.0.0")
    
    extension = ET.SubElement(addon, "extension")
    extension.set("point", "xbmc.addon.repository")
    extension.set("name", "WeebayModz Repository")
    
    info = ET.SubElement(extension, "info")
    info.text = "https://pckodiaddon.github.io/Kodiaddon/addons.xml"
    
    checksum = ET.SubElement(extension, "checksum")
    checksum.text = "https://pckodiaddon.github.io/Kodiaddon/addons.xml.md5"
    
    datadir = ET.SubElement(extension, "datadir")
    datadir.text = "https://pckodiaddon.github.io/Kodiaddon/zip"
    
    return ET.ElementTree(addon)

def create_repository():
    # Create directory structure
    base_dir = os.getcwd()
    repo_dir = os.path.join(base_dir, 'repository.weebaymodz')
    zip_dir = os.path.join(base_dir, 'zip')
    plugin_dir = os.path.join(base_dir, 'plugin.video.weebaymodz')
    
    # Create all necessary directories
    os.makedirs(repo_dir, exist_ok=True)
    os.makedirs(zip_dir, exist_ok=True)
    os.makedirs(plugin_dir, exist_ok=True)
    os.makedirs(os.path.join(plugin_dir, 'resources'), exist_ok=True)
    
    # Create basic addon.py
    addon_py_content = """import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

xbmcgui.Dialog().ok(addonname, "Hello from WeebayModz!")
"""
    
    with open(os.path.join(plugin_dir, 'addon.py'), 'w') as f:
        f.write(addon_py_content)
    
    # Create README.md
    readme_content = """# WeebayModz Kodi Repository

This repository contains the WeebayModz Kodi addon.

## Installation

1. Download the repository zip: [repository.weebaymodz-1.0.0.zip](zip/repository.weebaymodz-1.0.0.zip)
2. In Kodi, go to Settings > File Manager > Add source
3. Enter: `https://pckodiaddon.github.io/Kodiaddon`
4. Install from zip file
5. Install the addon from the repository

## Available Addons

- WeebayModz Video Addon
"""
    
    with open(os.path.join(base_dir, 'README.md'), 'w') as f:
        f.write(readme_content)
    
    # Create index.html
    index_html_content = """<!DOCTYPE html>
<html>
<head>
    <title>WeebayModz Kodi Repository</title>
</head>
<body>
    <h1>WeebayModz Kodi Repository</h1>
    <p>To install this repository, download <a href="zip/repository.weebaymodz-1.0.0.zip">repository.weebaymodz-1.0.0.zip</a> and install it in Kodi.</p>
    <p>Repository URL: https://pckodiaddon.github.io/Kodiaddon</p>
</body>
</html>"""
    
    with open(os.path.join(base_dir, 'index.html'), 'w') as f:
        f.write(index_html_content)
    
    # Create repository addon files
    repo_addon = create_repository_addon_xml()
    repo_addon.write(os.path.join(repo_dir, 'addon.xml'), encoding='utf-8', xml_declaration=True)
    
    # Create plugin addon files
    plugin_addon = create_addon_xml()
    plugin_addon.write(os.path.join(plugin_dir, 'addon.xml'), encoding='utf-8', xml_declaration=True)
    
    # Create combined addons.xml
    addons = ET.Element("addons")
    addons.append(repo_addon.getroot())
    addons.append(plugin_addon.getroot())
    
    addons_xml_path = os.path.join(base_dir, 'addons.xml')
    ET.ElementTree(addons).write(addons_xml_path, encoding='utf-8', xml_declaration=True)
    
    # Generate MD5
    md5 = generate_md5(addons_xml_path)
    with open(addons_xml_path + '.md5', 'w') as f:
        f.write(md5)
    
    # Create plugin ZIP
    with zipfile.ZipFile(os.path.join(zip_dir, 'plugin.video.weebaymodz-1.0.0.zip'), 'w') as zf:
        for root, dirs, files in os.walk(plugin_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, plugin_dir)
                zf.write(file_path, os.path.join('plugin.video.weebaymodz', arcname))
    
    # Create repository ZIP
    with zipfile.ZipFile(os.path.join(zip_dir, 'repository.weebaymodz-1.0.0.zip'), 'w') as zf:
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, repo_dir)
                zf.write(file_path, os.path.join('repository.weebaymodz', arcname))

if __name__ == "__main__":
    try:
        create_repository()
        print("\nRepository created successfully!")
        print("\nNext steps:")
        print("1. Commit and push all files to your repository")
        print("2. Enable GitHub Pages in repository settings (use main branch)")
        print("\nUsers can then install your repository using:")
        print("https://pckodiaddon.github.io/Kodiaddon/zip/repository.weebaymodz-1.0.0.zip")
    except Exception as e:
        print(f"Error creating repository: {str(e)}")