import os

ACHIEVEMENT_TEXT = 'achieveRow'
UNLOCKED_TEXT = 'unlocked'
TITLE_TAG = '<h3'
TITLE_END_TAG = '</h3>'
DESCRIPTION_TAG = '<h5'
DESCRIPTION_END_TAG = '</h5>'

def main():
    main_loop_condition = True

    while main_loop_condition:
        input_text, input_file_name = get_input()

        output_text = format_text(input_text)
        save_output(output_text, input_file_name)
        
        while True:
            print("Do you have any other file to format?\n Input y for yes, n for no.")
            input_text = input().strip().lower()

            if input_text == 'y' or input_text == 'yes':
                break
            elif input_text == 'n' or input_text == 'no':
                main_loop_condition = False
                break
            else:
                print("Please input a valid answer.\n")

def get_input():
    input_text = ''

    while True:
        print("Please enter the absolute path to the input file.\n")
        print("A valid input file is a Steam achievement page saved as .html from a browser.\n")
        input_text = input()

        if os.path.exists(input_text) == True:
            input_file = open(input_text, encoding="utf-8")

            input_file_name = os.path.basename(input_text)
            input_file_name = input_file_name[:input_file_name.find(os.path.splitext(input_text)[1])]
            input_text = input_file.read()

            if input_text.find(ACHIEVEMENT_TEXT) != -1:
                return input_text, input_file_name
            else:
                print("Invalid input file. Try again.\n")
        else:
            print("File location is invalid or file doesn't exist.")

def format_text(input_text):
    output_text = ''

    achievement_index = input_text.find(ACHIEVEMENT_TEXT)
    while True:
        line_text = ''

        # Append achievement completion state.
        status_index = input_text[achievement_index:].find(UNLOCKED_TEXT)
        if status_index == len(ACHIEVEMENT_TEXT) + 1:
            line_text += 'TRUE'
        else:
            line_text += 'FALSE'
        line_text += ','

        # Append achievement name.
        line_text += "\""
        line_text += input_text[
            achievement_index + input_text[achievement_index:].find(TITLE_TAG) + 
            input_text[achievement_index + input_text[achievement_index:].find(TITLE_TAG):].find('>') + 1: 
            achievement_index + input_text[achievement_index:].find(TITLE_END_TAG)]
        line_text += "\""
        line_text += ','

        # Append achievement description.
        line_text += "\""
        line_text += input_text[
            achievement_index + input_text[achievement_index:].find(DESCRIPTION_TAG) + 
            input_text[achievement_index + input_text[achievement_index:].find(DESCRIPTION_TAG):].find('>') + 1: 
            achievement_index + input_text[achievement_index:].find(DESCRIPTION_END_TAG)]
        line_text += "\""

        print(line_text)
        output_text += line_text

        next_achievement_index = input_text[achievement_index + len(ACHIEVEMENT_TEXT):].find(ACHIEVEMENT_TEXT)
        if next_achievement_index != -1:
            output_text += '\n'
            achievement_index = achievement_index + len(ACHIEVEMENT_TEXT) + next_achievement_index
        else:
            return output_text

def save_output(output_text, input_file_name):
    file = open('./output/' + input_file_name + '.csv', 'w')
    file.write(output_text)

if __name__ == "__main__":
    main()