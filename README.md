<h1 align="center">
    make_selection
  <br>
</h1>

Utility for interactive cli menus

## file.py
```python
from make_selection import makeSelection

options = ["one", "two", "three"]
label = "choose option"
selected = makeSelection(options, label)
```

## output
```sh
user@host:~$ python file.py
```
![make selection sample](/images/sample.png)
