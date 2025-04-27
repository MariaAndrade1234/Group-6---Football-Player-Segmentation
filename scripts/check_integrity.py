required_extensions = {'.jpg', '.jpeg', '.png', '.json', '.txt', '.yaml'}

def check_extensions(directory):
    missing = []
    for root, _, files in os.walk(directory):
        for file in files:
            if not any(file.lower().endswith(ext) for ext in required_extensions):
                missing.append(os.path.join(root, file))
    return missing