def readSecrets():
    secrets = [None] * 4

    with open('.secret') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line = line.strip()
        title, val = line.split(': ')
        secrets[i] = val
    
    return secrets
    
