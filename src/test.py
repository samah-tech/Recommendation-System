import config
print(hasattr(config, 'SMTP_PORT'))  # Should print: True
print(config.SMTP_PORT)  # Should print: 465 (or your defined port)
print(config.__file__)  # Shows which config.py is being imported