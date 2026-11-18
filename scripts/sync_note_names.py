"""Refresh name-only placeholders from the catalogue and documented taxonomy."""
from note_files import DATA, load_note_banks, read_json, save_note_banks, synchronize_names


def main():
    banks = load_note_banks()
    synchronize_names(banks, read_json(DATA / 'species.json'),
                      read_json(DATA / 'learning-taxonomy.json'))
    save_note_banks(banks)
    print('Names synchronized; existing notes and catalogue IDs preserved.')


if __name__ == '__main__':
    main()
