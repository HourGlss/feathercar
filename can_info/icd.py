icd = {
    1: {  # DEVICE MANUAL CON
        "name": "Manual control",
        "description": "Puts information from controller onto bus",
        "messages": {
            1: {  # MSG NUMBER
                "struct_string": "bb",
                "keywords": ["steering", "throttle"],
                "id": 0x010  # CAN BUS ID
            }
        }
    },
    8: {  # DEVICE TESTING
        "name": "test",
        "description": "Puts SOMETHING on the bus",
        "messages": {
            1: {  # MSG NUMBER
                "struct_string": "b",
                "keywords": ["number"],
                "id": 0x710  # CAN BUS ID
            }
        }
    }
}


def get_list_of_used_ids():
    for device, data_per_device in icd.items():
        for message_number, details_of_message in data_per_device['messages'].items():
            print(f"{hex(data_per_device['messages'][message_number]['id']):>4},\t {data_per_device['name']}")


if __name__ == "__main__":
    get_list_of_used_ids()
