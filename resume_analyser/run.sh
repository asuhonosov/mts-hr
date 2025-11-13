$(poetry env activate) && \
  PYTHONPATH=~/git/mts-hr/ streamlit run resume_analyser/app.py --server.port=8502 --server.address=0.0.0.0
