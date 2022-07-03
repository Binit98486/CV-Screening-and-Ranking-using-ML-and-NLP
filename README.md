ABSTRACT
A typical job posting on the Internet receives a massive number of applications within a short window of time. Manually filtering out the CVs is not practically possible as it takes a lot of time and incurs huge costs that the hiring companies cannot afford to bear. In addition, this process of screening CVs is not fair as many suitable profiles don’t get enough consideration which they deserve. This may result in missing out on the right candidates or selection of unsuitable applicants for the job. Using NLP (Natural Language Processing) and ML(Machine Learning) to screen and rank the CVs according to the given constraint, this intelligent system will screen and rank the CV of any format according to the given constraints or the following requirement provided by the client company. We will basically take the bulk of input CV from the client company and that client company will also provide the requirement and the constraints according to which the CV should be ranked by our system. Then those CVs are screened and ranked according to the job requirements.  The dataset used was public data from Kaggle  and Github which was downloaded from their website. 80% of the CV were used for training and 20% were used for testing purpose. The proposed system use Support Vector Machine model to train and test the data. The system implements Natural Language processing to process the resumes. System accepts resumes and CVs in pdf and doc format. On testing, Support Vector Machine model provided 96.89% accuracy on testing data and on training, it provided 98.96% accuracy.


First install all requirements
pip install -r requirements.txt

change path of the folder of 
Job_discription and Employee_resume

Then run flask
