import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

from datastore.models import Message


def get_tv_nb_clr():
    print('Getting classifier')
    ftr_tr, ftr_tt, lbl_tr, lbl_tt = train_test_split(
        list(
            Message.objects.values_list('normalized_text', flat=True).order_by(
                'id')),
        list(Message.objects.values_list('label', flat=True).order_by('id')),
        test_size=0.25, random_state=0
    )
    print('Data split')
    tv = TfidfVectorizer(ngram_range=(1, 2), stop_words='english').fit(ftr_tr)
    print('Vectorizer fit')
    ftr_tr_mtx = tv.transform(ftr_tr)
    print('Training data transformed')
    ftr_tt_mtx = tv.transform(ftr_tt)
    print('Testing data transformed', ftr_tr_mtx.shape)
    nb_clr = LinearSVC().fit(ftr_tr_mtx, lbl_tr)
    print('Classifier fit')
    nb_predictions = nb_clr.predict(ftr_tt_mtx)
    print('Test predictions done')
    nb_cm = confusion_matrix(lbl_tt, nb_predictions)
    print('Matrix created')
    with open('nb_clr_model', 'wb') as f:
        pickle.dump(nb_clr, f)
    with open('tv_model', 'wb') as f:
        pickle.dump(tv, f)
    print('CM:\n', nb_cm)
    print('Hooray!!!')
    return tv, nb_clr


# from sklearn.linear_model import LogisticRegression
# from sklearn.naive_bayes import GaussianNB
# nb_clr = GaussianNB().fit(ftr_tr_mtx, lbl_tr)
# nb_clr = SVC(probability=True).fit(ftr_tr_mtx, lbl_tr)
# nb_clr = LogisticRegression().fit(ftr_tr_mtx, lbl_tr)


