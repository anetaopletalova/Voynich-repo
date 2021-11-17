from datetime import datetime
import pandas
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from server.db.models import Page, Classification, Marking, Description


class Descriptio:
    def __init__(self, description):
        self.description = description

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Identification:
    def __init__(self, class_id, x, y, width, height, description):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description
        self.class_id = class_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def import_classifications(file_name, date_from):
    engine = create_engine('postgresql+psycopg2://postgres:admin@localhost:5433/postgres')
    s = Session(bind=engine)
    markings = []
    descriptions = []
    classifications = []

    # exported classification.csv
    data = pandas.read_csv(file_name)
    for index, row in data.iterrows():

        # filter out dates before selected date
        created = row['created_at']

        parsed_created_at = datetime.strptime(created[0:10], "%Y-%m-%d")
        if parsed_created_at < date_from:
            continue

        annotations = pandas.read_json(row['annotations'])
        an_data = json.loads(annotations.to_json())

        file = pandas.read_json(row['subject_data'])
        file_data = json.loads(file.to_json())
        filename = pandas.DataFrame(file_data.values())['Filename'][0]
        classif_id = row['classification_id']
        # najit podle fileName odpovidajici ID stranky v DB
        page_file = Page.query.filter_by(name=filename).first()
        # FIX
        if page_file is not None:
            new_classification = Classification(
                id=classif_id,
                page_id=page_file.id
            )
            classifications.append(new_classification)
        # na jedne strance jeden clovek co vse udelal - ulozit to Classification
        # do Description a Marking pak uz konkretni ohodnoceni s classification_id odpovidajici tomuto (mozna i page_id)

        # '0' for task 0 , '1' for task 1
        x = pandas.DataFrame(an_data['value']['0'])
        if len(pandas.DataFrame(an_data['value']['0'])) > 0:
            data_classifications = an_data['value']['0']
            page_description = an_data['value']['1']

            if classif_id is None:
                print(classif_id)

            for classification in data_classifications:
                new_marking = Marking(
                    classification_id=classif_id,
                    page_id=page_file.id,
                    x=classification['x'],
                    y=classification['y'],
                    width=classification['width'],
                    height=classification['height'],
                    description=list(classification['details'][0].values())[0])
                markings.append(new_marking)
                # if filename in data_dictionary:
                #     data_dictionary[filename].append(new_marking.toJSON())
                # else:
                #     data_dictionary[filename] = [new_marking.toJSON()]
            if page_description != '':
                new_description = Description(
                    page_id=page_file.id,
                    classification_id = classif_id,
                    description = page_description,
                )
                descriptions.append(new_description)
                # data_dictionary[filename].append(description_text.toJSON())

    # for key, values in data_dictionary.items():
    #     print(key)
    #     for value in values:
    #         print(value)

    # with open('data.json', 'w', encoding='utf-8') as f:
    #     json.dump(data_dictionary, f, ensure_ascii=False, indent=4)

    # s.bulk_save_objects(classifications)
    s.commit()
    s.bulk_save_objects(markings)
    s.bulk_save_objects(descriptions)
    s.commit()

    return
