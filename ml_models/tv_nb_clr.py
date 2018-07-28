import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

from datastore.models import Message


def get_tv_nb_clr():
    print('Getting classifier')
    ftr_tr, ftr_tt, lbl_tr, lbl_tt = train_test_split(
        list(Message.objects.values_list('normalized_text', flat=True).order_by('id')),
        list(Message.objects.values_list('label', flat=True).order_by('id')),
        test_size=0.25, random_state=0
    )
    print('data split')
    tv = TfidfVectorizer(ngram_range=(1, 2), stop_words='english').fit(ftr_tr)
    print('vectorizer fit')
    ftr_tr_mtx = tv.transform(ftr_tr)
    print('training transformed')
    ftr_tt_mtx = tv.transform(ftr_tt)
    print('testing transformed', ftr_tr_mtx.shape)
    nb_clr = LinearSVC().fit(ftr_tr_mtx, lbl_tr)
    print('nb fit')
    nb_predictions = nb_clr.predict(ftr_tt_mtx)
    print('predictions done')
    nb_cm = confusion_matrix(lbl_tt, nb_predictions)
    print('matrix created')
    with open('tv_nb_clr_model', 'wb') as f:
        pickle.dump(nb_clr, f)
    print('hooray!!!')
    print('CM:\n', nb_cm)
    return tv, nb_clr
