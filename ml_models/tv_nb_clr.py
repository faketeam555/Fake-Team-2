from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from datastore.models import Message


def get_tv_nb_clr():
    ftr_tr, ftr_tt, lbl_tr, lbl_tt = train_test_split(
        list(Message.objects.values_list('normalized_text', flat=True).order_by('id')),
        list(Message.objects.values_list('label', flat=True).order_by('id')),
        test_size=0.01, random_state=0
    )
    tv = TfidfVectorizer(ngram_range=(1, 2), stop_words='english').fit(ftr_tr)
    ftr_tr_mtx = tv.transform(ftr_tr)
    ftr_tt_mtx = tv.transform(ftr_tt)
    nb_clr = GaussianNB().fit(ftr_tr_mtx.todense(), lbl_tr)
    nb_predictions = nb_clr.predict(ftr_tt_mtx.todense())
    nb_cm = confusion_matrix(lbl_tt, nb_predictions)
    print('CM:\n', nb_cm)
    return tv, nb_clr
