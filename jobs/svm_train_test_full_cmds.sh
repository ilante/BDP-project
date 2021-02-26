#################################################
# Second run:
#################################################
svm-train -c 2 -g 0.5 -m 2000 /data2/in_train_tiny/train1.svm /data2/svm_outputs/train/train1.model && \
svm-predict /data2/in_predict_tiny/test1.svm /data2/svm_outputs/train/train1.model /data2/svm_outputs/predict/prediction1.out