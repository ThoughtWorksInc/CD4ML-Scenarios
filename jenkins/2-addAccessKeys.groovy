import jenkins.model.Jenkins
import com.cloudbees.plugins.credentials.domains.Domain
import org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl
import com.cloudbees.plugins.credentials.CredentialsScope
import hudson.util.Secret

instance = Jenkins.instance
domain = Domain.global()
store = instance.getExtensionList("com.cloudbees.plugins.credentials.SystemCredentialsProvider")[0].getStore()

def getSecret(String key) {
    String environmentKey = System.getenv(key)
    if (environmentKey == null) {
        throw new Exception("No " + key + "configured")
    }
}

secretAccessKey = new StringCredentialsImpl(
  CredentialsScope.GLOBAL,
  "ACCESS_KEY",
  "S3 Bucket Access Key",
  Secret.fromString(getSecret("ACCESS_KEY"))
)
store.addCredentials(domain, secretAccessKey)

secretKey = new StringCredentialsImpl(
  CredentialsScope.GLOBAL,
  "SECRET_KEY",
  "S3 Bucket Secret Key",
  Secret.fromString(getSecret("SECRET_KEY"))
)
store.addCredentials(domain, secretKey)

println "---> Created Minio Access Keys"