from editor.option_file import OptionFile

# Put PES 5 Option File in the same folder as this script
of_file_location = r"BASLUS-21685P2K8OPT"
of_file_location = r"BESLES-54913P2K8OPT"
of_file_location = r"PES2008OPTION FILE.psu"
of_file_location = r"we10.xps"
# Load/decrypt the option file
print("Loading option file...")
of = OptionFile(of_file_location)
print("Option file loaded.")

with open("temp.bin", "wb") as binary_file:
    binary_file.write(of.data)