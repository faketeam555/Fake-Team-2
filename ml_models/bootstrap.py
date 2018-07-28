import pandas

from spellchecker import SpellChecker

from django.utils import timezone

from datastore.models import Message
from ml_models.utils import normalize

data_frame = pandas.read_csv(
    'ml_models/corpus.txt', sep='\t', names=['Fake', 'Message']
)

for index, row in data_frame.iterrows():
    if type(row['Message']) == float:
        row['Message'] = ''

    normalized = normalize(row['Message'])

    spell = SpellChecker()
    spell_corrected = ''
    for word in normalized.split(' '):
        spell_corrected += (' ' + spell.correction(word))
    unknowns = ''
    for word in spell.unknown(normalized.split(' ')):
        unknowns += (' ' + word)

    Message.objects.create(
        full_text=row['Message'],
        label='N' if row['Fake'] else 'F',
        is_confirmed=True,
        updated_at=timezone.now(),
        normalized_text=normalized,
        spell_corrected_text=spell_corrected,
        unknown_words=unknowns
    )
