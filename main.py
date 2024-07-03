import json

def update_input_tf(akash_file, input_tf_file):
    # Load akash.json
    with open(akash_file, 'r') as f:
        akash_data = json.load(f)
    
    # Load input.tf
    with open(input_tf_file, 'r') as f:
        input_tf_data = f.readlines()

    # Update variables in input.tf
    updated_lines = []
    for line in input_tf_data:
        if line.strip().startswith('variable'):
            variable_name = line.split('"')[1]  # Extract variable name
            for chart in akash_data['charts']:
                chart_name = chart['chart']
                version = chart['version']
                if variable_name == chart_name:
                    updated_line = f' default = "{version}"\n'
                    line = line.replace(line.split('=')[1].strip(), updated_line.strip())
                    break
        updated_lines.append(line)

    # Write updated input.tf
    with open(input_tf_file, 'w') as f:
        f.writelines(updated_lines)

if __name__ == "__main__":
    akash_file = "akash.json"
    input_tf_file = "Terraform/input.tf"
    update_input_tf(akash_file, input_tf_file)
