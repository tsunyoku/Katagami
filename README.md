# Katagami
Katagami is a Python 3.9 file uploader, using Quart and cmyui_pkg.

## Installation
Linux:
```bash
git clone https://github.com/tsunyoku/Katagami.git
mv ext/requirements.txt requirements.txt
python3.9 -m pip install -r requirements.txt && rm -rf requirements.txt
mv ext/config.sample.py config.py # Edit your config.py file with a text editor of your choice.
```

Windows:
```bash
git clone https://github.com/tsunyoku/Katagami.git
COPY "ext\requirements.txt" requirements.txt
pip install -r requirements.txt
COPY "ext\config.sample.py" config.py # Edit your config.py file with a text editor of your choice.
```

## Booting it up

```python
python3.9 main.py, or
hypercorn main.py -b 127.0.0.1:9823 # Change :9823 to the port that you specified in config.py and ensure your NGINX config matches
```

## Contributing
PRs are more than welcome, and we'd love to see new contributors! Also, feel free to create an issue, we'll try our best :]

## License
Licensed under the `Do What The F*ck You Want To Public License`. Learn more [here](http://www.wtfpl.net).
