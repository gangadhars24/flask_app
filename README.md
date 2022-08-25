# Deploying Flask Application into Azure VM

### Creating python virtual environment
```python3 -m venv <venv_name>```

### Activating python virtual environment
```source <venv_name>/bin/activate```

### Running Flask Server/application
```python3 app.py```

### To access the flask application through local system browser
Create a inbound traffic rules to open the port in the VM
Then type the url in the local system browser like ```http://<public_ip_address_of_vm>:5000```