# diacritics_mapping

## Building

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
(venv) $ pip install --requirement requirements.txt
(venv) $ ./diacritics_mapping.py > diacritics_mapping_dict.go 
(venv) $ go vet
(venv) $ go build . && ./diacritics_mapping -shouldDebug true "Hello World"
```
