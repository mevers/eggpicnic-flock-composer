# Eggpicnic flock composer

Use this app to help choose your birds before ordering a flock composition from
[Eggpicnic](https://eggpicnic.com/create-your-own-flock-australia/). Try different
combinations of five to ten Australian birds, see how they look together and save
a picture of your favourites.

## Get started

1. Click the green **Code** button on this page, then **Download ZIP**.
2. Unzip the download and double-click **index.html** to open the app. Keep the files together in their folder.
3. Drag birds into the preview and rearrange them. Click **Download PNG** to save your picture.

The preview is approximate. Place your order directly with Eggpicnic.
All bird artwork belongs to Eggpicnic.

## Update the collection

The app comes with birds ready to use. To download the latest collection from
Eggpicnic, you’ll need Python installed. Open a terminal in the app’s folder.

The first time only, set up the tools needed to prepare the pictures:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install Pillow
```

Then update the collection with one command:

```sh
.venv/bin/python update_catalogue.py
```

This downloads the bird artwork and prepares it for the app. When it finishes,
reopen `index.html` to see the updated collection.
