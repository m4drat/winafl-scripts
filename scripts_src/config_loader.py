import json

def load_config(path):
    args = None
    try:
        cfg = open(path).read()
        args = json.loads(cfg)
    except FileNotFoundError:
        print('[-] Config file not found!')
    except json.decoder.JSONDecodeError as e: 
        print('[-] Config file isn\'t correct!')
        print(e)
    
    return args

if __name__ == "__main__":
    pass