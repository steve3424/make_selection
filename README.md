<h1 align="center">
    make_selection
  <br>
</h1>

<p align="center">
    Utility for interactive cli menus
  <br>
</p>

### Sample
#### file.py
```python
from make_selection import makeSelection

options = ["one", "two", "three"]
label = "choose option"
selected = makeSelection(options, label)
```

#### Show menu
![image of cli while using the menu](/images/using_menu.png)

#### After selection
![image of cli after item is selected](/images/item_selected.png)
