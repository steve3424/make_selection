<p align="center">
  <img src="https://raw.githubusercontent.com/steve3424/make_selection/develop/images/logo.png" alt="Make selection logo">
</p>


## Setup
```
pip install make_selection
```

## Sample
#### file.py
```python
from make_selection import makeSelection

options = ["one", "two", "three"]
label = "choose option"
selected = makeSelection(options, label)
```

#### Interacting with menu
<img src="https://raw.githubusercontent.com/steve3424/make_selection/develop/images/using_menu.png" alt="image of cli while using the menu">
<br>

#### After making selection
<img src="https://raw.githubusercontent.com/steve3424/make_selection/develop/images/item_selected.png" alt="image of cli after item is selected">
