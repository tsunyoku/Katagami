# Katagami
Katagami is a Python 3.9 file uploader, using Quart and cmyui_pkg.

## Installation

```python
git clone https://github.com/tsunyoku/Katagami.git
pip3 install -r requirements.txt
mv ext/config.sample.py config.py # After this, edit your config.py file with a text editor of your choice.
```

## Booting it up

```python
python3.9 main.py, or
hypercorn main.py -b 127.0.0.1:9823 # Change :9823 to the port that you specified in config.py
```

## Contributing
PRs are more than welcome, and we'd love to see new contributors! Also, feel free to create an issue, we'll try our best :]

## License
No license, do what the fuck you want with the code. We could care less
