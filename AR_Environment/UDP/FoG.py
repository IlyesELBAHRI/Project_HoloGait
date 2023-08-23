def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

while True:
    user_input = input("Press 'f' to write '0' or 'g' to write '1': ")

    if user_input == 'f':
        write_to_file("config.txt", "0")
        print("Successfully wrote '0' to config.txt.")
        break
    elif user_input == 'g':
        write_to_file("config.txt", "1")
        print("Successfully wrote '1' to config.txt.")
        break
    else:
        print("Please press 'f' or 'g'.")
