# minor project created on 12-04-2020 - Rishabh Sharma

from django.shortcuts import render
# render for the display of screen
from django.core.files.storage import FileSystemStorage
# filesystem storage for the file handling
from django.conf import settings
#  settings for the accessing the current directory for file handling
path_main=settings.BASE_DIR
# path main represents the current accessing directory some time it is required to have complete path so we use this


def index(request):
    return render(request,'mysite/index.html')
# it rander the index page
def resin(request):
    if request.method=='POST':
        upf=request.FILES['resume']
        # print(upf.name,upf.size)
        fs=FileSystemStorage()
        name=fs.save(upf.name,upf)
        context={}
        try:
            def result(path):
                import re
                import tika
                from tika import parser
                import pandas as pd
                from sklearn.feature_extraction.text import CountVectorizer
                parse = parser.from_file(path)
                resume = parse['content']
                res = resume.split("\n")
                skills = ['it skills', 'key skills', 'professional skills', 'expertise', 'skills', 'mastery',
                          'skills & achievement', 'skills & achievements', 'skill', 'language skill', 'computer skills',
                          'language and skills', 'skills & abilities', 'computer skill']
                df = pd.read_excel(path_main+ r'\media\headings.xlsx')
                headings = df['headings']
                copy_headings = []
                for i in headings:
                    copy_headings.append(i)
                for i in range(len(res)):
                    if ":" in res[i] or "\n" in res[i]:
                        try:
                            hed = re.findall(r'[\w\s]+', res[i])
                            for j in hed:
                                if j.lower() in copy_headings and j.lower() in skills:
                                    d = [res[i + 1]]
                        except:
                            context['error_code']='Sorry Resume not clear!!'
                            return ""

                def rezoom(d):
                    p = pd.read_csv(path_main+r'\media\career.csv')
                    documents = []
                    jobs = []
                    for i in range(0, 1194):
                        j = str(p.iloc[i:i + 1, 0:6]).lower()
                        k = str(p.iloc[i:i + 1, 6:7]).lower()
                        k = re.search(r'[a-z]+[\w\s]*', k)
                        j = re.search(r'[\d]{6}[\s\w.#\d+-]*', j)
                        try:
                            docs = j.group()
                        except:
                            pass
                        skill = docs[7:]
                        documents.append(skill)
                        jobs.append(k.group())
                    return zoom(d, documents, jobs)

                def zoom(d, documents, jobs):
                    # Create the Document Term Matrix
                    count_vectorizer = CountVectorizer(stop_words='english')
                    count_vectorizer = CountVectorizer()
                    recommend = {}
                    for i in d:
                        for j in documents:
                            sparse_matrix = count_vectorizer.fit_transform([i, j])

                            doc_term_matrix = sparse_matrix.todense()
                            df = pd.DataFrame(doc_term_matrix,
                                              columns=count_vectorizer.get_feature_names(),
                                              index=['i', 'j'])

                            from sklearn.metrics.pairwise import cosine_similarity
                            mat = cosine_similarity(df, df)
                            if mat[0][1] * 100 > 30:
                                if jobs[documents.index(j)] in recommend and recommend[jobs[documents.index(j)]] < \
                                        mat[0][1] * 100 > 30:
                                    recommend[jobs[documents.index(j)]] = int(round(mat[0][1] * 100, 2))
                                else:
                                    recommend[jobs[documents.index(j)]] = int(round(mat[0][1] * 100, 2))
                    return sorted(recommend.items(), key=lambda kv: (kv[1], kv[0]))

                x = rezoom(d)
                if type(x) == list:
                    x = x[::-1]
                    return (x[0:5])
                elif type(x) == str:
                    return x

            path = fs.path(name)
            k=result(path)
        except:
            context['error_code']='file is not supported'
            k=''
        context['data']=k
        fs.delete(name)
        return render(request, 'mysite/outputres.html',context)
    return render(request,'mysite/resinp.html')
def output(request):
    if request.method=='POST':
        return render(request,'mysite/outputres.html')