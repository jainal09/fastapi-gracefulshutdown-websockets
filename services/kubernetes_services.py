import os

def is_running_in_kubernetes() -> bool:
    return 'KUBERNETES_SERVICE_HOST' in os.environ

def get_pod_name() -> str:
    if is_running_in_kubernetes():
        return f"POD Name Space: {os.environ.get('KUBE_POD_NAMESPACE')} \
                POD Name: {os.environ.get('KUBE_POD_NAME')}"
    else:
        return "Not running inside Kubernetes"
    