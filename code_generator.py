import json
import re

class card_data(object):  
  def __init__(self):
    self.img = ''
    self.title = ''
    self.description = ''
  
  def set_img(self,img):
    self.img = img
  
  def set_title(self,title):
    self.title = title
  
  def set_description(self,description):
    self.description = description

def generate_css(settings):      
      row_width = settings['cards-per-row'] * (settings['card-width'] + 30)

      # Open the template of the CSS file to make modifications
      with open('flipbox_template.css', 'r') as template:
        # Read entire content of the file
        template_content = template.read()
        
        # Replace the items that are based on calculation and not on input
        template_content = template_content.replace('%row-width%', str(row_width))

        # Replace all the macros with their relevant settings
        matches = re.findall(r'%([\w-]+)%', template_content)
        for match in matches:
          template_content = template_content.replace('%{}%'.format(match), str(settings[match]))
        
        # Dump the new template content to file
        with open('flipbox.css', 'w') as outfile:
          outfile.write(template_content)

def parse_card_data():
  with open('cards.data', 'r') as cards_data:
    file_content = cards_data.read()
    cards_data = filter(None, file_content.split('[card]\n'))
    cards = []
    for card in cards_data:
      params = card.split("\n\n")
      card_entry = card_data()
      card_entry.set_img(params[0])
      card_entry.set_title(params[1])
      card_entry.set_description(params[2])
      cards.append(card_entry)

    return cards

def generate_html(settings):
  cards = parse_card_data()

  with open('card_template.html','r') as card_template_file:
    card_template = card_template_file.read()
    cards_blocks = '<div class="cards-row">'
    cards_count = 0

    for card in cards:
      new_card = card_template
      new_card = new_card.replace('%img_path%', card.img)
      new_card = new_card.replace('%front-card-text%', card.title)
      new_card = new_card.replace('%back-card-title%', card.title)
      new_card = new_card.replace('%back-card-text%', card.description)

      cards_blocks = cards_blocks + new_card
      cards_count = cards_count+1
      
      if (cards_count % settings['cards-per-row'] == 0):
        cards_blocks = cards_blocks + '</div><div class="cards-row">'


    cards_blocks = cards_blocks + '</div>'

    with open('flipbox_template.html', 'r') as flipbox_template:
      template_content = flipbox_template.read()
      template_content = template_content.replace("<cards/>", cards_blocks)

      with open('flipbox.html', 'w') as output:
        output.write(template_content)

def main():
  # Open JSON file for reading
  with open('settings.json', 'r') as json_file:
      # Read JSON file to dictionary
      settings = json.load(json_file)

      generate_css(settings)
      generate_html(settings)

if __name__== "__main__":
  main()