https://www.youtube.com/watch?v=k9-Pw0v0Cjw

https://bitnami.com/stack/mongodb/helm
https://jhooq.com/convert-kubernetes-yaml-into-helm/s

helm repo add bitnami https://charts.bitnami.com/bitnami
Helm show values bitnami/mongodb > values.yml
Edit the file
helm install my-mongodb bitnami/mongodb

Helm create spingboot or any name
