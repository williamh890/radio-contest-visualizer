
from sys import argv
import json


class ConactParseError(Exception):
    pass


def contact_to_dict(info_list):
    tags = ["frequency",
            "mode",
            "date",
            "utc_time",
            "callsign",
            "serial_number",
            "presidence",
            "check",
            "section",
            "callsign",
            "serial_number",
            "presidence",
            "check",
            "section"]

    if len(info_list) != len(tags):
        print(len(info_list), len(tags))
        raise Exception('wrong number of input args')
    pairs = list(zip(tags, info_list))

    metadata = {tag: val for tag, val in pairs[:4]}
    operator = {tag: val for tag, val in pairs[4:9]}
    contact = {tag: val for tag, val in pairs[9:]}

    return {
        **metadata,
        "operator": operator,
        "contact": contact
    }


class ContactDataParser(object):
    def __init__(self):
        self.file_loaded = False
        self.contacts = []
        self.metadata = []

    def fromFile(self, file_path):
        with open(file_path) as f:
            raw_data = f.read()
        self.file_loaded = True

        self._parse(raw_data)

        return self.contacts, self.metadata

    def _parse(self, raw_data):
        for line in raw_data.split("\n"):
            if "END-OF-LOG" in line:
                break

            self._parse_line(line)

        print(f"{len(self.contacts)} total contacts")
        print(f"{json.dumps(self.contacts[0], indent=2)}")

    def _parse_line(self, line):
        try:
            self._parse_contact(line)
        except ConactParseError:
            self._parse_metadata(line)

    def _parse_contact(self, line):
        key, contact = line.split(':')
        contact_data = [d for d in contact.split(' ') if d != '']

        if len(contact_data) != 14:
            raise ConactParseError()

        self.contacts.append(
            contact_to_dict(contact_data)
        )

    def _parse_metadata(self, meta):
        name, value = meta.split(':')

        self.metadata.append({
            'name': name,
            'value': value
        })


def parse_contact_data(path):
    return ContactDataParser().fromFile(path)


def write_to_file(file_path, meta, contacts):
    json_log = json.dumps(meta, indent=2) + '\n' + \
        json.dumps(contacts, indent=2)

    with open(file_path, 'w') as f:
        f.write(json_log)


if __name__ == "__main__":
    if len(argv) == 1:
        print(
            "python contact-data-parser [input_file_path] [output_file_path]"
        )
        exit(1)

    try:
        input_file_path = argv[1]
    except IndexError:
        print("file name required as command line arg.")
    else:
        metadata, contact_data = parse_contact_data(input_file_path)

    try:
        output_file_path = argv[2]
    except IndexError:
        print("file name required to write to json")
    else:
        write_to_file(output_file_path, metadata, contact_data)
