from json import dumps as json_dumps


def render_human(hemoglobin):
    for grammarbot_file in hemoglobin.files:
        print(grammarbot_file.f.name)
        for match in grammarbot_file.matches:
            print(f"\tSentence: {match.sentence}")
            print(f"\t\tMessage: {match.message}")
            print("\t\tPossible corrections:")
            for correction in match.corrections:
                print(f"\t\t\t{correction}")
            print("\t\tDetail:")
            print(f"\t\t\tType: {match.type}")
            print(f"\t\t\tCategory: {match.category}")
            print(f"\t\t\tRule: {match.rule}")
    print(
        f"Number of API calls made: {hemoglobin.grammarbot.api_calls_made}"
    )


def render_json(hemoglobin):
    print(json_dumps(hemoglobin.to_dict()))