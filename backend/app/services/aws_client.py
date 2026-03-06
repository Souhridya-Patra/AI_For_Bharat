"""AWS service clients."""
import boto3
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AWSClient:
    """AWS service client manager."""
    
    def __init__(self):
        """Initialize AWS clients."""
        self.session = boto3.Session(
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        
        self._sagemaker_runtime = None
        self._s3 = None
        self._dynamodb = None
        self._comprehend = None
    
    @property
    def sagemaker_runtime(self):
        """Get SageMaker Runtime client."""
        if self._sagemaker_runtime is None:
            self._sagemaker_runtime = self.session.client('sagemaker-runtime')
        return self._sagemaker_runtime
    
    @property
    def s3(self):
        """Get S3 client."""
        if self._s3 is None:
            self._s3 = self.session.client('s3')
        return self._s3
    
    @property
    def dynamodb(self):
        """Get DynamoDB resource."""
        if self._dynamodb is None:
            self._dynamodb = self.session.resource('dynamodb')
        return self._dynamodb
    
    @property
    def comprehend(self):
        """Get Amazon Comprehend client."""
        if self._comprehend is None:
            self._comprehend = self.session.client('comprehend')
        return self._comprehend


# Global AWS client instance
aws_client = AWSClient()
