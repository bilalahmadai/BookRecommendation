from flask import Flask,render_template,request
app=Flask(__name__)


import numpy as np
import pickle
# print(pickle.__version__)
popular_df=pickle.load(open('popular_df.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
final_rating=pickle.load(open('final_rating_book.pkl','rb'))
@app.route('/')
def index():
    return render_template('index.html',book_name=list(popular_df['Book-Title'].values),
                    rating=list(popular_df['avgrating'].values),
                    author=list(popular_df['Book-Author_x'].values),
                    image=list(popular_df['Image-URL-M_x'].values),
                    vote=list(popular_df['num_of_rating'].values),
                    )


	
	
@app.route('/recommend',methods=["POST"])
def  recommend():
    
    user_input=request.form.get('user_input')
    show=request.form.get('show')
    print(str(user_input))
    print(type(int(show)))



    p=pt.index==user_input
    if p[p].size>0:
        index=np.where(pt.index==user_input)[0][0]
        similar_book= sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:int(show)]
        data=[]
        for i in similar_book:
            items=[]
            df_temp=final_rating[final_rating['Book-Title']==pt.index[i[0]]]
            items.extend(list(df_temp.drop_duplicates('Book-Title')['Book-Title'].values))
            items.extend(list(df_temp.drop_duplicates('Book-Title')['Book-Author'].values))
            items.extend(list(df_temp.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(items)
    else:

        data=[]
        print("empty")
        print(data)


    # print(data)
    return render_template('search.html',data=data)
  

if __name__=='__main__':
    app.run()