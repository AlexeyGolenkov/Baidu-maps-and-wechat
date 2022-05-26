# Baidu-maps-and-wechat

## Parsing

Run

```python3 parse.py```

Then write what you want to search in Chinese (for example '房产公司' - real estate agency).

Wait for a while.

## Mailing

Run

```python3 messaging.py```

Follow the instruction. If it says "press 'add' button" then find where the 'add' button is placed and click on it three times. When you complete all steps,
the program will start mailing.

Once you did that, button positions are saved in config file and you don't need to do setting again. If you want to change button positions - run

```python3 messaging.py set_new=True```
