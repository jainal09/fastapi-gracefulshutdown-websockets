import os


def is_running_in_kubernetes() -> bool:
    """
    Check if the application is running inside a Kubernetes cluster
    Args:
        None
    Returns:
        bool: True if running inside Kubernetes, False otherwise
    """
    return 'KUBERNETES_SERVICE_HOST' in os.environ

def get_pod_name() -> str:
    """
    Get the name of the pod and the namespace if running inside Kubernetes
    Args:
        None
    Returns:
        str: Pod name and namespace if running inside Kubernetes, otherwise a message
    """
    if is_running_in_kubernetes():
        return f"POD Name Space: {os.environ.get('KUBE_POD_NAMESPACE')} \
                POD Name: {os.environ.get('KUBE_POD_NAME')}"
    else:
        return "Not running inside Kubernetes"
