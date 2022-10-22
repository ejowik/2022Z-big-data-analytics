# Big Data Analytics

## Environment setup - references
- [Dataproc | Google Cloud](https://cloud.google.com/dataproc) 
- [Dataproc Flink component](https://cloud.google.com/dataproc/docs/concepts/components/flink)
- [1.5.x release versions | Dataproc Documentation | Google Cloud](https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-release-1.5) 
- [Apache Spark and Jupyter Notebooks on Cloud Dataproc](https://www.google.com/url?q=https://codelabs.developers.google.com/codelabs/spark-jupyter-dataproc%230&sa=D&source=docs&ust=1666439162833914&usg=AOvVaw0YKYT9riwRh6Qighgf3Q5J)
    - customized code:
    ```REGION=europe-central2
    ZONE=europe-central2-a
    CLUSTER_NAME=cluster-bda4
    BUCKET_NAME=data-potential-366306-spark-jupyter
    ```
    ```
    gcloud beta dataproc clusters create ${CLUSTER_NAME} \
     --region=${REGION} \
     --image-version=1.5 \
     --master-machine-type=n1-standard-4 \
     --worker-machine-type=n1-standard-4 \
     --bucket=${BUCKET_NAME} \
     --optional-components=JUPYTER,ANACONDA,ZOOKEEPER,HBASE,FLINK \
     --enable-component-gateway
    ```
- [How to setup Nifi on Google Cloud Platform (2022)](https://www.youtube.com/watch?v=V6YVx_qDFnI)
