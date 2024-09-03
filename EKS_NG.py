#Code-1
"""
import boto3
import os

# Initialize boto3 EKS client
eks_client = boto3.client('eks')

# Define EKS cluster and node group names from environment variables
EKS_CLUSTER_NAME = os.environ['EKS_CLUSTER_NAME']
NODE_GROUP_NAME = os.environ['NODE_GROUP_NAME']

def lambda_handler(event, context):
    try:
        # Fetch the current node group configuration
        response = eks_client.describe_nodegroup(
            clusterName=EKS_CLUSTER_NAME,
            nodegroupName=NODE_GROUP_NAME
        )
        
        # Extract the current scaling configuration
        scaling_config = response['nodegroup']['scalingConfig']
        current_desired = scaling_config['desiredSize']
        
        # Determine the action from the payload
        action = event.get('action', '').lower()  # Extract action from event payload

        # Define target configurations based on action
        if action == 'scale_down' or (not action and current_desired != 0):
            # Scale down to desired and min size of 0, but max size must be at least 1
            target_config = {
                'desiredSize': 0,
                'minSize': 0,
                'maxSize': 1  # EKS requires maxSize to be at least 1
            }
            action_taken = 'Scaled down'
        elif action == 'scale_up' or (not action and current_desired == 0):
            # Scale up to desired configuration
            target_config = {
                'desiredSize': 2,
                'minSize': 1,
                'maxSize': 3
            }
            action_taken = 'Scaled up'
        else:
            # Invalid action handling
            return {
                'statusCode': 400,
                'body': 'Invalid action. Use "scale_up" or "scale_down".'
            }
        
        # Update the node group with the new configuration
        eks_client.update_nodegroup_config(
            clusterName=EKS_CLUSTER_NAME,
            nodegroupName=NODE_GROUP_NAME,
            scalingConfig=target_config
        )

        # Log the action
        log_message = (f"{action_taken} node group '{NODE_GROUP_NAME}' "
                       f"to DesiredSize: {target_config['desiredSize']}, "
                       f"MinSize: {target_config['minSize']}, "
                       f"MaxSize: {target_config['maxSize']}.")

        print(log_message)

        return {
            'statusCode': 200,
            'body': log_message
        }

    except Exception as e:
        # Handle exceptions and return error message
        error_message = f"Error scaling node group: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': error_message
        }
"""

#Code-2        
"""
import boto3
import os

# Initialize boto3 clients
eks_client = boto3.client('eks')
sns_client = boto3.client('sns')

# Define EKS cluster, node group names, and SNS topic ARN from environment variables
EKS_CLUSTER_NAME = os.environ['EKS_CLUSTER_NAME']
NODE_GROUP_NAME = os.environ['NODE_GROUP_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Fetch the current node group configuration
        response = eks_client.describe_nodegroup(
            clusterName=EKS_CLUSTER_NAME,
            nodegroupName=NODE_GROUP_NAME
        )
        
        # Extract the current scaling configuration
        scaling_config = response['nodegroup']['scalingConfig']
        current_desired = scaling_config['desiredSize']
        
        # Determine the action from the payload
        action = event.get('action', '').lower()  # Extract action from event payload

        # Define target configurations based on action
        if action == 'scale_down' or (not action and current_desired != 0):
            # Scale down to desired and min size of 0, but max size must be at least 1
            target_config = {
                'desiredSize': 0,
                'minSize': 0,
                'maxSize': 1  # EKS requires maxSize to be at least 1
            }
            action_taken = 'Scaled down'
        elif action == 'scale_up' or (not action and current_desired == 0):
            # Scale up to desired configuration
            target_config = {
                'desiredSize': 2,
                'minSize': 1,
                'maxSize': 3
            }
            action_taken = 'Scaled up'
        else:
            # Invalid action handling
            return {
                'statusCode': 400,
                'body': 'Invalid action. Use "scale_up" or "scale_down".'
            }
        
        # Update the node group with the new configuration
        eks_client.update_nodegroup_config(
            clusterName=EKS_CLUSTER_NAME,
            nodegroupName=NODE_GROUP_NAME,
            scalingConfig=target_config
        )

        # Log the action
        log_message = (f"{action_taken} node group '{NODE_GROUP_NAME}' "
                       f"to DesiredSize: {target_config['desiredSize']}, "
                       f"MinSize: {target_config['minSize']}, "
                       f"MaxSize: {target_config['maxSize']}.")

        print(log_message)

        # Publish the message to SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"EKS Node Group Scaling - {action_taken}",
            Message=log_message
        )

        return {
            'statusCode': 200,
            'body': log_message
        }

    except Exception as e:
        # Handle exceptions and return error message
        error_message = f"Error scaling node group: {str(e)}"
        print(error_message)
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EKS Node Group Scaling Error",
            Message=error_message
        )
        return {
            'statusCode': 500,
            'body': error_message
        }
"""

"""

#Multiple Node Groups

import boto3
import os

# Initialize boto3 clients
eks_client = boto3.client('eks')
sns_client = boto3.client('sns')

# Define EKS cluster and SNS topic ARN from environment variables
EKS_CLUSTER_NAME = os.environ.get('EKS_CLUSTER_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
NODE_GROUPS = os.environ.get('NODE_GROUPS', '').split(',')  # Default to empty list if not set

if not EKS_CLUSTER_NAME or not SNS_TOPIC_ARN:
    raise ValueError("Required environment variables are missing: EKS_CLUSTER_NAME or SNS_TOPIC_ARN")

def lambda_handler(event, context):
    try:
        # Check if NODE_GROUPS is empty
        if not NODE_GROUPS:
            raise ValueError("NODE_GROUPS environment variable is not set or is empty")

        # Determine the action from the payload
        action = event.get('action', '').lower()  # Extract action from event payload

        # Define target configurations based on action
        if action == 'scale_down':
            target_config = {
                'desiredSize': 0,
                'minSize': 0,
                'maxSize': 1  # EKS requires maxSize to be at least 1
            }
            action_taken = 'Scaled down'
        elif action == 'scale_up':
            target_config = {
                'desiredSize': 2,
                'minSize': 1,
                'maxSize': 3
            }
            action_taken = 'Scaled up'
        else:
            # Invalid action handling
            return {
                'statusCode': 400,
                'body': 'Invalid action. Use "scale_up" or "scale_down".'
            }

        # Iterate over each node group and update the configuration
        for node_group_name in NODE_GROUPS:
            try:
                # Fetch the current node group configuration
                response = eks_client.describe_nodegroup(
                    clusterName=EKS_CLUSTER_NAME,
                    nodegroupName=node_group_name
                )
                
                # Update the node group with the new configuration
                eks_client.update_nodegroup_config(
                    clusterName=EKS_CLUSTER_NAME,
                    nodegroupName=node_group_name,
                    scalingConfig=target_config
                )

                # Log the action
                log_message = (f"{action_taken} node group '{node_group_name}' "
                               f"to DesiredSize: {target_config['desiredSize']}, "
                               f"MinSize: {target_config['minSize']}, "
                               f"MaxSize: {target_config['maxSize']}.")

                print(log_message)

                # Publish the message to SNS
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=f"EKS Node Group Scaling - {action_taken}",
                    Message=log_message
                )
                
            except Exception as e:
                # Handle exceptions for individual node groups
                error_message = (f"Error scaling node group '{node_group_name}': {str(e)}")
                print(error_message)
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="EKS Node Group Scaling Error",
                    Message=error_message
                )

        return {
            'statusCode': 200,
            'body': f"Scaling action '{action_taken}' applied to node groups: {', '.join(NODE_GROUPS)}."
        }

    except Exception as e:
        # Handle exceptions and return error message
        error_message = f"Error scaling node groups: {str(e)}"
        print(error_message)
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EKS Node Group Scaling Error",
            Message=error_message
        )
        return {
            'statusCode': 500,
            'body': error_message
        }

        
""" 


#Lambda function to handle different scaling configurations for each node group. 
import boto3
import os
import re

# Initialize boto3 clients
eks_client = boto3.client('eks')
sns_client = boto3.client('sns')

# Define EKS cluster and SNS topic ARN from environment variables
EKS_CLUSTER_NAME = os.environ['EKS_CLUSTER_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

# Define scaling configurations for each node group
SCALING_CONFIGURATIONS = {
    'myEKS01-NG': {
        'scale_down': {'desiredSize': 0, 'minSize': 0, 'maxSize': 1},
        'scale_up': {'desiredSize': 1, 'minSize': 1, 'maxSize': 2}
    },
    'test2ndng': {
        'scale_down': {'desiredSize': 0, 'minSize': 0, 'maxSize': 1},
        'scale_up': {'desiredSize': 2, 'minSize': 2, 'maxSize': 3}
    },
}

# Regular expression for valid node group names
VALID_NODEGROUP_NAME_PATTERN = re.compile(r'^[0-9A-Za-z][A-Za-z0-9-_]*$')

def lambda_handler(event, context):
    try:
        # Ensure NODE_GROUPS is not empty
        node_groups = os.environ.get('NODE_GROUPS', '').split(',')
        if not node_groups or all(not ng.strip() for ng in node_groups):
            raise ValueError('NODE_GROUPS environment variable is not set or empty.')
        
        # Check for action in event
        action = event.get('action', '').lower()
        if action not in ['scale_up', 'scale_down']:
            return {
                'statusCode': 400,
                'body': 'Invalid action. Use "scale_up" or "scale_down".'
            }
        
        for nodegroup_name in node_groups:
            nodegroup_name = nodegroup_name.strip()
            
            # Skip empty node group names
            if not nodegroup_name:
                continue

            # Validate node group name
            if not VALID_NODEGROUP_NAME_PATTERN.match(nodegroup_name):
                error_message = f"Invalid node group name: '{nodegroup_name}'."
                print(error_message)
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="EKS Node Group Scaling Error",
                    Message=error_message
                )
                continue
            
            try:
                # Fetch the current node group configuration
                response = eks_client.describe_nodegroup(
                    clusterName=EKS_CLUSTER_NAME,
                    nodegroupName=nodegroup_name
                )
                
                # Define target configurations based on action
                if action == 'scale_down':
                    target_config = SCALING_CONFIGURATIONS.get(nodegroup_name, {}).get('scale_down')
                elif action == 'scale_up':
                    target_config = SCALING_CONFIGURATIONS.get(nodegroup_name, {}).get('scale_up')

                if not target_config:
                    print(f"No scaling configuration found for node group {nodegroup_name} with action {action}.")
                    continue

                # Update the node group with the new configuration
                try:
                    update_response = eks_client.update_nodegroup_config(
                        clusterName=EKS_CLUSTER_NAME,
                        nodegroupName=nodegroup_name,
                        scalingConfig=target_config
                    )

                    # Log the response for debugging
                    print(f"Update response for {nodegroup_name}: {update_response}")

                    # Check for successful update response
                    if update_response.get('update', {}).get('status') not in ['InProgress', 'Successful']:
                        print(f"Update not successful for {nodegroup_name}: {update_response}")
                        continue

                    log_message = f"Scaled node group {nodegroup_name} to DesiredSize: {target_config['desiredSize']}, MinSize: {target_config['minSize']}, MaxSize: {target_config['maxSize']}."
                    print(log_message)

                    sns_client.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Subject=f"EKS Node Group Scaling - {action} completed",
                        Message=log_message
                    )

                except Exception as e:
                    error_message = f"Error updating node group {nodegroup_name}: {str(e)}"
                    print(error_message)
                    sns_client.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Subject="EKS Node Group Scaling Error",
                        Message=error_message
                    )
            
            except Exception as e:
                error_message = f"Error describing node group {nodegroup_name}: {str(e)}"
                print(error_message)
                sns_client.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject="EKS Node Group Describe Error",
                    Message=error_message
                )

        return {
            'statusCode': 200,
            'body': 'Scaling actions completed successfully.'
        }

    except Exception as e:
        error_message = f"Error in Lambda function: {str(e)}"
        print(error_message)
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="EKS Node Group Scaling Error",
            Message=error_message
        )
        return {
            'statusCode': 500,
            'body': error_message
        }
