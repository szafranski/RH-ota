from pathlib import Path
import platform


# removes old aliases, especially doubled ones and bad leftovers from ~/.bashrc file
# part of action is done in script - has to be ported

def aliases_clean(start, end, file_name, *words):
    if platform.system() == "Linux":
        write_lines = []
        skipping = False
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if start in line:
                    skipping = True
                if not skipping:
                    write_lines.append(line)
                if end in line:
                    skipping = False
                for word in words:
                    if word in line:
                        write_lines.remove(line)

        with open(file_name, 'w') as write_obj:
            write_obj.write("".join(write_lines))
            return False
    else:
        pass


def main():
    home_dir = str(Path.home())
    Path(f"{home_dir}/.ota_markers").mkdir(exist_ok=True)
    aliases_clean('Shortcut', 'After', f'{home_dir}/.bashrc', 'uu', 'updateupdater', '# #')


if __name__ == "__main__":
    main()
