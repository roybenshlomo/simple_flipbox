import json
import re

def main():
  # Open JSON file for reading
  with open('settings.json', 'r') as json_file:
      # Read JSON file to dictionary
      settings = json.load(json_file)
      
      # Calculate number of rows and height of the rows
      num_of_rows = settings['number-of-cards'] / settings['cards-per-row']
      row_width = settings['cards-per-row'] * settings['card-width']

      # Open the template of the CSS file to make modifications
      with open('flipbox_template.css', 'r') as template:
        # Read entire content of the file
        template_content = template.read()
        
        # Replace the items that are based on calculation and not on input
        template_content = template_content.replace("%row-width%", str(row_width))

        # Replace all the macros with their relevant settings
        matches = re.findall(r'%([\w-]+)%', template_content)
        for match in matches:
          template_content = template_content.replace("%{}%".format(match), str(settings[match]))
        
        # Dump the new template content to file
        with open("flipbox.css", 'w') as outfile:
          outfile.write(template_content)

if __name__== "__main__":
  main()