
#run experiments
dvc init --subdir
dvc repro
     git add dvc.lock data/.gitignore
dvc exp run -S train.c0=1



#To enable auto staging, run:
dvc config core.autostage true

#Add remote
dvc remote add -d storage gdrive://0AIac4JZqHhKmUk9PDA
dvc remote modify myremote gdrive_client_id 'client-id'
dvc remote modify myremote gdrive_client_secret 'client-secret'

#Add data and experiments to dvc remote storage
dvc add data/cell_samples_for_svm.csv
        #To track the changes with git, run:
        git add data/cell_samples_for_svm.csv.dvc       data/.gitignore
