import math
from datetime import datetime
import pandas
import json
from server.db.database import db
from server.db.models import Page, Classification, Marking, Description
from server.utils.helpers import as_dict


def import_classifications(file_name):
    s = db.session
    markings = []
    descriptions = []
    classifications = []

    config_file = open("import_config.txt", "r+")
    last_date_value = config_file.readlines()[-1]
    last_date_value_parsed = datetime.strptime(last_date_value[0:19], "%Y-%m-%d %H:%M:%S")

    data = pandas.read_csv(file_name)
    for index, row in data.iterrows():
        created_at = row['created_at']

        # if last record, set into config
        if index == data.index[-1]:
            config_file.write("\n"+created_at)

        # filter out dates before selected date
        parsed_created_at = datetime.strptime(created_at[0:19], "%Y-%m-%d %H:%M:%S")

        if last_date_value_parsed and parsed_created_at < last_date_value_parsed:
            continue

        if parsed_created_at == last_date_value_parsed:
            continue

        annotations = pandas.read_json(row['annotations'])
        an_data = json.loads(annotations.to_json())

        file = pandas.read_json(row['subject_data'])
        file_data = json.loads(file.to_json())
        filename = pandas.DataFrame(file_data.values())['Filename'][0]
        classif_id = row['classification_id']
        user_id = row['user_id']
        user_name = row['user_name']

        page_file = Page.query.filter_by(name=filename).first()

        # '0' for task 0 , '1' for task 1
        m_to_save = []
        new_page_description = ''
        if len(pandas.DataFrame(an_data['value']['0'])) > 0:
            data_classifications = an_data['value']['0']
            page_description = an_data['value']['1']

            if classif_id is None:
                print(classif_id)

            # TODO check if it is possible to add ID here
            for classification in data_classifications:
                new_marking = Marking(
                    classification_id=classif_id,
                    page_id=page_file.id,
                    x=classification['x'],
                    y=classification['y'],
                    width=classification['width'],
                    height=classification['height'],
                    description=list(classification['details'][0].values())[0].rstrip("\n"))
                markings.append(new_marking)
                m_to_save.append(as_dict(new_marking))

            if page_description != '':
                new_description = Description(
                    page_id=page_file.id,
                    classification_id=classif_id,
                    description=page_description,
                )
                descriptions.append(new_description)
                new_page_description = page_description

        if page_file is not None:
            new_classification = Classification(
                id=classif_id,
                page_id=page_file.id,
                # check this, looks like its always -1
                user_id=int(user_id) if not math.isnan(user_id) else -1,
                user_name=user_name,
                created_at=created_at,
                markings=json.dumps(m_to_save),
                description=new_page_description
            )
            classifications.append(new_classification)

    config_file.close()
    s.bulk_save_objects(classifications)
    s.commit()
    s.bulk_save_objects(markings)
    s.bulk_save_objects(descriptions)
    s.commit()

    return
