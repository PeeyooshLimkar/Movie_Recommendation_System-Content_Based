FROM continuumio/anaconda3:2022.10

WORKDIR /pkl/projects/rec_sys/content_based/movie_rec_sys/

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 8501

CMD streamlit run app.py
