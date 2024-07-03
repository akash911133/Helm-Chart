import json
import os

def update_tf_variables(akash_json_path, input_tf_path):
    # Load akash.json
    with open(akash_json_path, 'r') as f:
        data = json.load(f)

    # Initialize a mapping from chart names to variable names
    chart_variable_mapping = {}

    # Update input.tf
    input_tf_full_path = os.path.join(input_tf_path, 'input.tf')
    with open(input_tf_full_path, 'r') as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        updated_line = line
        if line.strip().startswith('variable'):
            variable_name = line.strip().split('"')[1]
            if variable_name in chart_variable_mapping:
                latest_version = chart_variable_mapping[variable_name]
                updated_line = f'variable "{variable_name}" {{\n default = "{latest_version}"\n}}\n'
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    # Write updated input.tf
    with open(input_tf_full_path, 'w') as f:
        f.writelines(updated_lines)

    # Print the updated values (for GitHub Actions console output)
    for chart in data['charts']:
        chart_name = chart['chart']
        version = chart['version']
        chart_variable_mapping[chart_name] = version

        print(f"Updated {chart_name} to {version}")

# Define paths
akash_json_path = './akash.json'
terraform_dir_path = './Terraform'

# Call the function to update variables
update_tf_variables(akash_json_path, terraform_dir_path)

