# eks-nodegroup-scaling
Scale Up and Scale Down the Node Group of EKS

Update Environment Variable's in Lambda:
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

For EKS:
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"eks:DescribeNodegroup",
				"eks:UpdateNodegroupConfig",
				"eks:ListNodegroups"
			],
			"Resource": [
				"arn:aws:eks:ap-south-1:0000000000:cluster/my-eks-cluster01",
				"arn:aws:eks:ap-south-1:0000000000:nodegroup/my-eks-cluster01/*"
			]
		}
	]
}
```

For SNS:
```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "sns:Publish",
			"Resource": "arn:aws:sns:ap-south-1:000000000:EKS-Notification"
		}
	]
}
```

Setting the desired and minimum size to 0, while maintaining a minimum size of 1, provides a balance between cost efficiency and availability in an EKS cluster. By carefully considering these factors and implementing best practices, we can effectively manage our cluster's resources and ensure optimal performance.

