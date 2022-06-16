# cool-free-wallpapers

Having discovered that old oil paintings make the best desktop wallpapers I had 3 challenges:

1) Where to find high quality images of existing oil paintings
2) How to automate the downloads (I like to have constantly rotating wallpapers, so need many downloaded)
3) Which images to download given these are for wallpapers (aspect ratio sensitive)

The [The Metropolitan Museum of Art Collection API](https://metmuseum.github.io/) allows for all of this very easily.

## Notes

By going [here](https://www.metmuseum.org/art/collection/search?) you can see what images result from given search text, and then use that for your download.

User is prompted during runtime for number of images to download, desired search text, and desired MET department. The latter two have default values set to "Monet" and "European Paintings".

When the objects are retrieved only those which are Open Access and which have the correct aspect ratio are downloaded.

## To Run Locally

Clone the project

```bash
  git clone https://github.com/laurenceWalton/cool-free-wallpapers
```

Navigate to project directory

```bash
  cd cool-free-wallpapers
```

Run fetch.py

```python
  python3 fetch.py
```
