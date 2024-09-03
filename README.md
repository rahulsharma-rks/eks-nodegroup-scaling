# eks-nodegroup-scaling
Scale Up and Scale Down the Node Group of EKS

Update ENvironment Variable's in Lambda:
* EKS_CLUSTER_NAME: my-eks-cluster01
* NODE_GROUPS: myEKS01-NG,test2ndng
* SNS_TOPIC_ARN: arn:aws:sns:ap-south-1:00000000000:EKS-Notification

Permissions List:
* AmazonEC2ContainerRegistryReadOnly
* AmazonEC2FullAccess
* AmazonEKS_CNI_Policy
* AmazonEKSClusterPolicy
* AmazonEKSWorkerNodePolicy
* AWSLambdaBasicExecutionRole

