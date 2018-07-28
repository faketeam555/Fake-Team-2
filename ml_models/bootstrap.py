import pandas
import hashlib

from django.utils import timezone

from datastore.models import Message
from ml_models.utils import normalize

data_frame = pandas.read_csv(
    'ml_models/corpus.txt', sep='\t', names=['Fake', 'Message']
)

for index, row in data_frame.iterrows():
    if type(row['Message']) == float:
        row['Message'] = ''

    normal_text = normalize(row['Message'])
    Message.objects.create(
        full_text=row['Message'],
        label='F' if row['Fake'] else 'N',
        is_confirmed=True,
        is_real=False,
        updated_at=timezone.now(),
        normalized_text=normal_text,
        hash_value=hashlib.sha256(normal_text.encode('utf-8')).hexdigest()
    )
