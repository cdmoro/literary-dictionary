import petname
import sys
import pyperclip

def main():
    count = 1

    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass

    ids = [petname.generate(3, separator='-') for _ in range(count)]

    if count == 1:
        print(ids[0])
        pyperclip.copy(ids[0])
        print("ID copied to clipboard!")
    else:
        joined = '\n'.join(ids)
        print(joined)
        pyperclip.copy(joined)
        print(f"{count} IDs copied to clipboard!")
        
    # for index, id in enumerate(ids):
    #     print (f'UPDATE entries SET global_id = "{id}" WHERE rowid = {index + 1};')

if __name__ == "__main__":
    main()
