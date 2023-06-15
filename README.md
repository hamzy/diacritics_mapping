# diacritics_mapping

## Building

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install --requirement requirements.txt
(venv) $ ./diacritics_mapping.py > diacritics_mapping_dict.go  # Optional
(venv) $ go vet
(venv) $ go build . && ./diacritics_mapping -shouldDebug true "Hello World"
```

I have included `diacritics_mapping_dict.go` in the repository if the website
it was based on ( [Letters with diacritical marks, grouped alphabetically](https://pinyin.info/unicode/diacritics.html) ) 
disappears.  I have also removed some of the entries that didn't look enough like the original letter.
